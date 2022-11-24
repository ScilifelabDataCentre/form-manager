<template>
<q-page class="flex items-center justify-center">
  <q-table
    style="max-width: 97% ;min-width: 850px"
    title="Forms"
    :rows="entries"
    :columns="columns"
    row-key="identifier"
    :pagination="pagination"
    :filter="filter"
    :loading="loading"
    no-data-label="No entries found"
    :no-results-label="filter + ' does not match any entries'"
    >
    <template #top-right>
      <q-btn
	class="q-mx-sm"
	dense
	round
	outline
	icon="add"
	@click="addForm" />      
      <q-input v-model="filter" rounded outlined dense debounce="300" placeholder="Search">
        <template #append>
          <q-icon name="search" />
        </template>
      </q-input>
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
	<q-th auto-width />
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
	    @click="expandItem(props)"
            />
	</q-td>
        <q-td key="title" :props="props">
          {{ props.row.title }}
        </q-td>
        <q-td key="identifier" :props="props">
          {{ props.row.identifier }}
        </q-td>
        <q-td key="recaptcha" :props="props">
          <q-icon
	    :name="props.row.recaptcha_secret.length ? 'check_circle' : 'cancel'"
	    :color="props.row.recaptcha_secret.length ? 'positive' : 'negative'"
	    size="1.5em">
          </q-icon>
        </q-td>
        <q-td key="sendEmail" :props="props">
          <q-icon
	    :name="props.row.email_recipients.length ? 'check_circle' : 'cancel'"
	    :color="props.row.email_recipients.length ? 'accent' : 'secondary'"
	    size="1.5em">
          </q-icon>
        </q-td>
        <q-td key="redirect" :props="props">
          <q-icon
	    :name="props.row.redirect.length ? 'check_circle' : 'cancel'"
	    :color="props.row.redirect.length ? 'accent' : 'secondary'"
	    size="1.5em">
          </q-icon>
        </q-td>
	<q-td auto-width>
          <q-btn
            color="primary"
            icon="account_tree"
            size="sm"
            round
            dense
	    @click=gotoEntry(props.row.identifier)
            />
	</q-td>
      </q-tr>
      <q-tr v-if="props.expand" :props="props">
        <q-td colspan="100%">
	  <q-list dense>
            <q-item>
              <q-item-section>
		<q-input
		  v-model="editData[props.key].title"
		  dense
		  outlined
		  label="Title"
		  />
              </q-item-section>
            </q-item>
            <q-item>
              <q-item-section>
		<q-input
		  v-model="editData[props.key].redirect"
		  dense
		  outlined
		  label="Redirect to"
		  />
              </q-item-section>
            </q-item>
            <q-item>
              <q-item-section>
		<q-input
		  v-model="editData[props.key].recaptcha_secret"
		  dense
		  outlined
		  label="Recaptcha secret"
		  />
              </q-item-section>
            </q-item>
            <q-item>
              <q-item-section>
		<str-list-editor
		  v-model="editData[props.key].email_recipients"
		  field-title="Email Recipients"
		  />
              </q-item-section>
            </q-item>
	    <div v-show="editData[props.key].email_recipients.length > 0">
	    <q-item>
              <q-item-section>
		<q-input
		  v-model="editData[props.key].email_title"
		  dense
		  outlined
		  label="Email title"
		  />
              </q-item-section>
	    </q-item>
	    <q-item>
	      <q-item-section>
		<q-toggle
		  v-model="editData[props.key].email_custom"
		  label="Custom email template"
		  />
		<q-space />
		<div v-show="editData[props.key].email_custom">
		  <q-btn
		    flat
		    label="Edit text email"
		    @click="openTemplateDialog(editData[props.key], 'text')"
		    />
		  <q-btn
		    flat
		    label="Edit html email"
		    @click="openTemplateDialog(editData[props.key], 'html')"
		    />
		</div>
	      </q-item-section>
	    </q-item>
	    </div>
            <q-item>
              <q-item-section>
		<str-list-editor
		  v-model="editData[props.key].owners"
		  field-title="Form Owners"
		  :static-current-user="true"
		  />
              </q-item-section>
            </q-item>
	    <q-item>
	      <q-item-section>
		<div class="items-end">
		  <q-btn
		    flat
		    round
		    dense
		    size="md"
		    icon="check"
		    color="positive"
		    :loading="editData[props.key].saving"
		    @click="saveEdit(props)" />
		  <q-btn
		    flat
		    round
		    dense
		    bg-color="positive"
		    size="md"
		    icon="cancel"
		    color="negative"
		    @click="cancelEdit(props)" />
		  <q-btn
		    flat
		    round
		    dense
		    class="q-ml-md"
		    bg-color="positive"
		    size="md"
		    icon="delete"
		    color="negative"
		    @click="confirmDelete(props)" />
		  <span v-show="editData[props.key].saveError" class="text-negative">Save failed</span>
		</div>
	      </q-item-section>
	    </q-item>
	  </q-list>
        </q-td>
      </q-tr>
    </template>
  </q-table>
  <q-dialog v-model="showEditTemplateDialog">
    <q-card style="min-width: 600px">
      <q-card-section class="column">
	<div class="text-h5 q-mb-sm">Edit Email Template</div>
	<q-input
	  v-model="currentEditTemplateText"
	  autogrow
	  outlined
	  type="textarea"
	  />
      </q-card-section>

      <q-card-actions align="right">
        <q-btn
	  flat
          label="Keep"
          color="positive"
          @click="saveTemplate" />
        <q-btn
	  v-close-popup
	  flat
	  label="Cancel"
	  color="grey-7" />
      </q-card-actions>
    </q-card>
  </q-dialog>
  <q-dialog v-model="showDeleteWarning">
    <q-card>
      <q-card-section class="row items-center">
        <q-avatar icon="fas fa-trash" color="alert" text-color="primary" />
        <span class="q-ml-sm">Are you sure you want to delete this form?</span>
      </q-card-section>

      <q-card-actions align="right">
        <q-btn
	  flat
          :loading="isDeleting"
          label="Delete"
          color="negative"
          class="user-edit-confirm-delete"
          @click="deleteForm" />
        <q-btn
	  v-close-popup
	  flat
	  label="Cancel"
	  color="grey-7" />
      </q-card-actions>
    </q-card>
  </q-dialog>

</q-page>
</template>

<script>
import { defineComponent } from 'vue'

import StringListEditor from 'components/StringListEditor.vue'

export default defineComponent({
  name: 'FormBrowser',
  components: {
    'str-list-editor': StringListEditor,
  },

  data () {
    return {
      entries: [],
      editData: {},
      isDeleting: false,
      toDelete: {},
      filter: '',
      loading: false,
      loadError: false,
      showEditTemplateDialog: false,
      showDeleteWarning: false,
      currrentEditTemplate: {},
      currrentEditTemplateText: "",
      currrentEditTemplateType: "",
      pagination: {
        rowsPerPage: 20
      },
      columns: [
        {
          name: 'title',
          label: 'Title',
          field: 'title',
          required: true,
	  align: 'left',
          sortable: true
        },
        {
          name: 'identifier',
          label: 'Identifier',
          field: 'identifier',
          required: true,
          sortable: true,
        },
        {
          name: 'recaptcha',
          label: 'reCAPTCHA',
          field: 'recaptcha',
          required: true,
          sortable: true,
        },
        {
          name: 'sendEmail',
          label: 'Send email',
          field: 'email',
          required: true,
          sortable: true,
        },
        {
          name: 'redirect',
          label: 'Redirect',
          field: 'redirect',
          required: true,
          sortable: true,
        },
      ]
    }
  },

  mounted () {
    this.getEntries();
  },

  methods: {
    getEntries () {
      this.loading = true;
      this.$axios
	.get('/api/v1/form')
        .then((response) => {
	  this.entries = response.data['forms']
	})
      .catch((err) => {
	this.loadError = true;
      })
      .finally(() => this.loading = false);
    },
    gotoEntry(identifier) {
      this.$router.push({name: 'FormResponses', params: {identifier: identifier}});
    },

    confirmDelete(entry) {
      this.toDelete = entry;
      this.showDeleteWarning = true;
    },

    deleteForm() {
      this.isDeleting = true;
      this.$axios
	.delete('/api/v1/form/' + this.toDelete.row.identifier,
		{headers: {'X-CSRFToken': this.$q.cookies.get('_csrf_token')}})
        .then(() => {
	  this.toDelete.expand = false;
	  this.showDeleteWarning = false;
	  delete this.editData[this.toDelete.row.identifier];
	  this.getEntries();
	})
	.finally(() => this.isDeleting = false);
    },
    addForm() {
      this.$axios
	.post('/api/v1/form', {}, {headers: {'X-CSRFToken': this.$q.cookies.get('_csrf_token')}})
        .then(() => this.getEntries())
    },
    expandItem(entry) {
      entry.expand = !entry.expand;
      if (!(entry.key in this.editData)) {
	this.editData[entry.key] = {
	  title: entry.row.title,
	  recaptcha_secret: entry.row.recaptcha_secret,
	  email_recipients: JSON.parse(JSON.stringify(entry.row.email_recipients)),
	  email_custom: entry.row.email_custom,
	  email_text_template: entry.row.email_text_template,
	  email_html_template: entry.row.email_html_template,
	  email_title: entry.row.email_title,
	  owners: JSON.parse(JSON.stringify(entry.row.owners)),
	  redirect: entry.row.redirect,
	  saving: false,
	}
      }
    },
    saveEdit(entry) {
      this.editData[entry.key].saving = true;
      this.editData[entry.key].saveError = false;
      let outgoing = JSON.parse(JSON.stringify(this.editData[entry.key]));
      delete outgoing.saving;
      delete outgoing.saveError;
      this.$axios
	.patch('/api/v1/form/' + entry.row.identifier, outgoing, {headers: {'X-CSRFToken': this.$q.cookies.get('_csrf_token')}})
        .then((response) => {
	  entry.expand = false;
	  delete this.editData[entry.key];
	  this.getEntries();
	  })
	.catch((err) => {
	  this.editData[entry.key].saveError = true
	  this.editData[entry.key].saving = false
	})
    },
    cancelEdit(entry) {
      entry.expand = false;
      delete this.editData[entry.key];
    },
    openTemplateDialog(entry, type) {
      this.showEditTemplateDialog = true;
      let prop = "email_" + type + "_template";
      this.currentEditTemplate = entry;
      console.log(this.currentEditTemplate)
      this.currentEditTemplateType = prop;
      this.currentEditTemplateText = entry[prop];
    },
    saveTemplate() {
      this.currentEditTemplate[this.currentEditTemplateType] = this.currentEditTemplateText;
      this.showEditTemplateDialog = false;
    },
  },
})
</script>
