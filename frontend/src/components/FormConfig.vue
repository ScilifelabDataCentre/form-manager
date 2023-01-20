<template>
<div v-if="Object.keys(editData).length > 0">
  <q-list dense>
    <q-item>
      <q-item-section>
	<q-input
	  v-model="editData.identifier"
	  outlined
	  label="Identifier"
	  readonly
	  />
      </q-item-section>
    </q-item>

    <q-item>
      <q-item-section>
	<q-input
	  v-model="editData.title"
	  outlined
	  label="Title"
	  />
      </q-item-section>
    </q-item>

    <q-item>
      <q-item-section>
	<q-input
	  v-model="editData.redirect"
	  outlined
	  label="Redirect to"
	  />
      </q-item-section>
    </q-item>

    <q-item>
      <q-item-section>
	<q-input
	  v-model="editData.recaptcha_secret"
	  outlined
	  label="Recaptcha secret"
	  />
      </q-item-section>
    </q-item>

    <q-item>
      <q-item-section>
	<str-list-editor
	  v-model="editData.email_recipients"
	  field-title="Email Recipients"
	  />
      </q-item-section>
    </q-item>

    <div v-show="editData.email_recipients.length > 0">
      <q-item>
        <q-item-section>
	  <q-input
	    v-model="editData.email_title"
	    outlined
	    label="Email title"
	    />
        </q-item-section>
      </q-item>
      <q-item>
	<q-item-section>
	  <q-toggle
	    v-model="editData.email_custom"
	    label="Use custom email templates"
	    />
	  <q-space />
	  <transition
	    appear
	    enter-active-class="animated fadeIn"
	    leave-active-class="animated fadeOut"
	    >
	    <div
	      v-show="editData.email_custom"
	      class="flex justify-between item-stretch content-stretch">
	      <q-input
		v-model="editData.email_text_template"
		class="col-6"
		style="min-width: 49%"
		autogrow
		outlined
		type="textarea"
		label="Email text template"
		/>
	      <q-input
		v-model="editData.email_html_template"
		class="col-6"
		style="min-width: 49%"
		autogrow
		outlined
		type="textarea"
		label="Email HTML template"
		/>
	    </div>
	  </transition>
	</q-item-section>
      </q-item>
    </div>
    <q-item>
      <q-item-section>
	<str-list-editor
	  v-model="editData.owners"
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
	    :loading="editData.saving"
	    @click="save" />
	  <q-btn
	    flat
	    round
	    dense
	    bg-color="positive"
	    size="md"
	    icon="refresh"
	    color="accent"
	    @click="getEntry" />
	  <q-btn
	    flat
	    round
	    dense
	    class="q-ml-md"
	    bg-color="positive"
	    size="md"
	    icon="delete"
	    label="Delete form"
	    color="negative"
	    @click="confirmDelete(props)" />
	  <span v-show="editData.saveError" class="text-negative">Save failed</span>
	</div>
      </q-item-section>
    </q-item>
  </q-list>
  <q-dialog v-model="showEditTemplateDialog">
    <q-card style="min-width: 600px">
      
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
  <q-dialog v-model="showAbandonWarning">
    <q-card>
      <q-card-section class="row items-center">
        <q-avatar icon="fas fa-trash" color="alert" text-color="primary" />
        <span class="q-ml-sm">Are you sure you want to abandon your changes?</span>
      </q-card-section>
      
      <q-card-actions align="right">
        <q-btn
	  v-close-popup
	  flat
          label="Yes"
          color="negative"
          class="user-edit-confirm-delete"
          @click="deleteForm" />
        <q-btn
	  flat
	  label="Continue editing"
	  color="grey-7" />
      </q-card-actions>
    </q-card>
  </q-dialog>
</div>
</template>

<script>
import { defineComponent } from 'vue'

import StringListEditor from 'components/StringListEditor.vue'

export default defineComponent({
  name: 'FormConfig',
  components: {
    'str-list-editor': StringListEditor,
  },

  props: {
    identifier: {
      type: String,
      required: true,
    }
  },

  emits: ['form-deleted'],

  data () {
    return {
      entry: {},
      editData: {},
      isDeleting: false,
      toDelete: {},
      loading: false,
      loadError: false,
      showEditTemplateDialog: false,
      showDeleteWarning: false,
    }
  },

  computed : {
    dataChanged: {
      get () {
	return this.entry != this.editData;
      }
    }
  },

  mounted () {
    this.getEntry();
  },
  
  methods: {
    getEntry() {
      this.loading = true;
      this.$api
	.get('/form/' + this.identifier)
        .then((response) => {
	  this.entry = response.data['form']
	  this.editData = JSON.parse(JSON.stringify(this.entry))
	})
      .catch((err) => {
	this.loadError = true;
      })
      .finally(() => this.loading = false);
    },

    confirmDelete(entry) {
      this.toDelete = entry;
      this.showDeleteWarning = true;
    },

    deleteForm() {
      this.isDeleting = true;
      this.$api
	.delete('/form/' + this.identifier,
		{headers: {'X-CSRFToken': this.$q.cookies.get('_csrf_token')}})
        .then(() => {
	  this.showDeleteWarning = false;
	  delete this.editData;
	  delete this.entry;
	  this.$emit('form-deleted');
	})
	.finally(() => this.isDeleting = false);
    },

    save() {
      this.saving = true;
      this.saveError = false;
      let outgoing = JSON.parse(JSON.stringify(this.editData));
      this.$api
	.patch('/form/' + this.identifier,
	       outgoing,
	       {headers: {'X-CSRFToken': this.$q.cookies.get('_csrf_token')}}
	      )
        .then((response) => {
	  this.getEntry();
	})
	.catch((err) => {
	  this.saveError = true
	  this.saving = false
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
