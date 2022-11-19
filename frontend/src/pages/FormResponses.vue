<template>
<q-page class="fit column justify-center items-center content-center">
  <q-btn
    label="Back to Form Browser"
    icon="arrow_back"
    class="q-my-lg"
    color="primary"
    :to="{ name: 'FormBrowser' }"
    />
  
  <q-card
    v-if="Object.keys(urlInfo).length > 0"
    class="q-my-sm">
    <q-card-section>
      &lt;form action="{{ urlInfo.submission_url }}" method="{{ urlInfo.method }}" accept-charset="utf-8"&gt;
    </q-card-section>
  </q-card>
  
  <q-table
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
	<q-td>
	  <q-btn
	    v-if="listingType === 'submission'"
	    color="red"
	    icon="delete"
	    flat
	    @click="deleteSubmission(props.row.id)"
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
</q-page>
</template>

<script>
import { defineComponent } from 'vue'
import { copyToClipboard } from 'quasar'

export default defineComponent({
  name: 'FormSubmissions',
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
    deleteSubmission(subid) {
      this.$axios
	.delete('/api/v1/form/' + this.identifier + '/submission/' + subid,
	       {headers: {'X-CSRFToken': this.$q.cookies.get('_csrf_token')}})
        .then(() => this.getEntry())
	.catch(() => console.log('Failed to delete entry ' + subid))
    }
  },
})
</script>
