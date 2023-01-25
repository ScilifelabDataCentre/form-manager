<template>
<q-page class="flex items-start justify-center q-mt-xl">
  <div v-if="selected.length === 0">
    <transition
      appear
      enter-active-class="animated fadeIn"
      leave-active-class="animated fadeOut"
      >
      <form-browser
	v-model="selected"
	:refresh-needed="refreshNeeded"
	@refresh-done="refreshNeeded = false" />
    </transition>
  </div>
  <div v-else>
    <transition
      appear
      enter-active-class="animated fadeIn"
      leave-active-class="animated fadeOut"
      >
      <div style="min-width: 850px">
	<div class="q-my-md">
	  <q-btn
	    rounded
	    icon="arrow_back"
	    label="Choose another form"
	    size="l"
	    @click="getLeaveConfirmation" />
	</div>
	<q-card>
	  <q-tabs
	    v-model="tab"
	    dense
	    class="text-grey"
	    active-color="primary"
	    indicator-color="primary"
	    align="justify"
	    >
	    <q-tab name="config" label="Configuration" />
	    <q-tab name="submissions" label="Submissions" />
	  </q-tabs>
	  
	  <q-separator />
	  
	  <q-tab-panels v-model="tab" animated>
	    <q-tab-panel name="config">
	      <form-config
		:identifier="selected"
		@form-deleted="leaveForm" />
	    </q-tab-panel>
	    
	    <q-tab-panel name="submissions">
	      <form-submissions :identifier="selected" />
	    </q-tab-panel>
	  </q-tab-panels>
	</q-card>
      </div>
    </transition>
  </div>
  <q-btn
    class="q-ma-md"
    icon="add"
    label="Add new form"
    color="primary"
    @click="addForm" />

  <q-dialog v-model="showLeaveFormDialog">
    <q-card>
      <q-card-section class="row items-center">
        <q-avatar icon="warning" text-color="negative" />
        <span class="q-ml-sm">Are you sure you want to abandon you changes to the form?</span>
      </q-card-section>
      
      <q-card-actions align="right">
        <q-btn
	  v-close-popup
	  flat
          label="Yes"
          color="primary"
	  class="confirm-leave"
          @click="leaveForm" />
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

import FormBrowser from 'components/FormBrowser.vue'
import FormConfig from 'components/FormConfig.vue'
import FormSubmissions from 'components/FormSubmissions.vue'

export default defineComponent({
  name: 'FormHandler',

  components: {
    'form-browser': FormBrowser,
    'form-config': FormConfig,
    'form-submissions': FormSubmissions,
  },
  
  data () {
    return {
      selected: '',
      tab: 'config',
      refreshNeeded: false,
      showLeaveFormDialog: false,
    }
  },

  methods: {
    getLeaveConfirmation () {
      this.showLeaveFormDialog = true
    },

    leaveForm () {
      this.selected = ''
      this.tab = 'config'
    },

    addForm() {
      this.$api
	.post('/form', {}, {headers: {'X-CSRFToken': this.$q.cookies.get('_csrf_token')}})
        .then(() => this.refreshNeeded = true);
    },

  }
})
</script>
