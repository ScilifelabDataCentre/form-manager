<template>
<div>
  <q-card
    v-if="Object.keys(urlInfo).length > 0"
    bordered
    class="q-my-sm">
    <q-card-section>
      &lt;form action="{{ urlInfo.submission_url }}" method="{{ urlInfo.method }}" accept-charset="utf-8"&gt;
    </q-card-section>
  </q-card>
  
  <q-table
    flat
    class="q-my-lg"
    :title="formInfo.title"
    :rows="listingType === 'submission' ? rawSubmissions : questions"
    :columns="listingType === 'submission' ? columnsSubmission : columnsQuestion"
    :pagination="pagination"
    row-key="id"
    >
    <template #top-right>
      <q-btn-toggle
        v-model="listingType"
        class="q-mx-md"
        no-caps
        rounded
        unelevated
        toggle-color="primary"
        color="white"
        text-color="primary"
        :options="[
                  {label: 'By submission', value: 'submission'},
                  {label: 'By question', value: 'question'}
                  ]"
        />
    </template>
    <template #header="props">
      <q-tr :props="props">
        <q-th auto-width />
        <q-th
          v-for="col in props.cols"
          :key="col.name"
          :props="props"
          >
          {{ col.label }}
        </q-th>
      </q-tr>
    </template>
    
    <template #body="props">
      <q-tr :props="props">
        <q-td auto-width>
          <q-btn
            color="primary"
            :icon="props.expand ? 'expand_less' : 'expand_more'"
            size="sm"
            round
            dense
	    @click="props.expand = !props.expand"
            />
        </q-td>
        <q-td
          v-for="col in props.cols"
          :key="col.name"
          :props="props"
          >
          {{ col.value }}
        </q-td>
	<q-td auto-width>
	  <q-btn
	    v-if="listingType === 'submission'"
	    color="red"
	    icon="delete"
	    flat
	    round
            dense
	    @click="confirmDelete(props.row.id)"
	    />
	</q-td>
      </q-tr>
      <q-tr v-show="props.expand" :props="props">
        <q-td colspan="100%">
          <q-scroll-area style="height: 250px; max-width: 100%;">
            <q-markup-table
	      v-if="listingType === 'submission'"
	      :wrap-cells="true" flat
	      >
              <thead>
              </thead>
              <tbody>
		<tr
		  v-for="value, key in props.row.submission"
		  :key="key"
		  >
                  <td class="text-weight-bold text-left">
                    {{ key }}
                  </td>
                  <td>
                    {{ value }}
                  </td>
		</tr>
              </tbody>
            </q-markup-table>
            <q-markup-table v-else flat>
              <thead>
              </thead>
              <tbody>
		<tr
		  v-for="value, i in props.row.submissions"
		  :key="i">
                  <td>
                    {{ value }}
                  </td>
		</tr>
              </tbody>
            </q-markup-table>
          </q-scroll-area>
        </q-td>
      </q-tr>
    </template>
  </q-table>

  <q-btn
    label="Copy JSON to clipboard"
    icon="content_copy"
    class="q-my-lg"
    color="secondary"
    @click="jsonToClipboard(listingType === 'submission' ? rawSubmissions : questions)"
    />

  <delete-dialog
    v-model="showDeleteWarning"
    entry-type="submission"
    @delete-confirmed="deleteSubmission" />
</div>
</template>

<script>
import { defineComponent } from 'vue'
import { copyToClipboard } from 'quasar'

import DeleteDialog from 'components/DeleteDialog.vue'

export default defineComponent({
  name: 'FormSubmissions',

  components: {
    'delete-dialog': DeleteDialog,
  },
  
  props: {
    identifier: {
      type: String,
      required: true,
    }
  },

  data () {
    return {
      formInfo: {},
      currentTab: "submission",
      submissionPagination: {
        rowsPerPage: 10
      },
      pagination: {
        rowsPerPage: 10
      },
      columnsSubmission: [
        {
          name: 'id',
          label: 'ID',
          field: 'id',
          required: true,
          sortable: true
        },
        {
          name: 'timestamp',
          label: 'Timestamp',
          field: 'timestamp',
          required: true,
          sortable: true
        },
      ],
      columnsQuestion: [
        {
          name: 'question',
          label: 'Question',
          field: 'id',
          required: true,
          sortable: true
        },
	{
          name: 'submissionCount',
          label: 'Submission Count',
          field: 'count',
          required: true,
          sortable: true
        },

      ],
      rawSubmissions: [],
      submissionsLoading: false,
      submissionsError: false,
      infoLoading: false,
      infoError: false,
      urlLoading: false,
      urlError: false,
      urlInfo: {},
      listingType: 'submission',
      showCopyInfo: false,
      toDelete: {},
      showDeleteWarning: false,
    }
  },

  computed: {
    questions: {
      get () {
        let outData = [];
	let tmpData = {};
	for (let entry of this.rawSubmissions) {
	  for (let key in entry.submission) {
	    if (!entry.submission[key].length)
	      continue
	    if (key in tmpData) {
	      tmpData[key].push(entry.submission[key]);
	    }
	    else {
	      tmpData[key] = [entry.submission[key]];
	    }
	  }
	}
	for (let key in tmpData)
	  outData.push({id: key, submissions: tmpData[key], count: tmpData[key].length})
	return outData;
      }
    },
  },

  mounted () {
    this.getEntry()
  },

  methods: {
    jsonToClipboard (submissionData) {
      copyToClipboard(JSON.stringify(submissionData))
	.then(() => {
	  // success!
	})
	.catch(() => {
	  // fail
	})
      this.$q.notify({
        group: false,
        message: 'JSON copied to clipboard.',
        color: 'primary'
      })
    },
    getEntry () {
      this.submissionsLoading = true;
      this.submissionsError = false;
      this.$axios
	.get('/api/v1/form/' + this.identifier + '/submission')
        .then((submission) => this.rawSubmissions = submission.data.submissions)
	.catch(() => this.submissionsError = true)
	.finally(() => this.submissionsLoading = false);
      this.infoLoading = true;
      this.infoError = false;
      this.$axios
	.get('/api/v1/form/' + this.identifier)
        .then((submission) => this.formInfo = submission.data.form)
	.catch((err) => this.infoError = true)
      	.finally(() => this.infoLoading = false);
      this.urlLoading = true;
      this.urlError = false;
      this.$axios
	.get('/api/v1/form/' + this.identifier + '/url')
        .then((submission) => this.urlInfo = submission.data)
	.catch((err) => this.urlError = true)
      	.finally(() => this.urlLoading = false);
    },

    confirmDelete(entry) {
      this.toDelete = entry;
      this.showDeleteWarning = true;
    },

    deleteSubmission() {
      this.$axios
	.delete('/api/v1/form/' + this.identifier + '/submission/' + this.toDelete,
	       {headers: {'X-CSRFToken': this.$q.cookies.get('_csrf_token')}})
        .then(() => this.getEntry())
	.catch(() => console.log('Failed to delete entry ' + subid))
    }
  },
})
</script>
