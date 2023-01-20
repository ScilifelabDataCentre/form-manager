<template>
<q-page class="flex items-start justify-center q-mt-xl">
  <div v-if="selected.length === 0">
    <transition
      appear
      enter-active-class="animated fadeIn"
      leave-active-class="animated fadeOut"
      >
      <form-browser v-model="selected" />
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
	    @click="leaveForm" />
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
		@form-deleted="leaveForm()" />
	    </q-tab-panel>
	    
	    <q-tab-panel name="submissions">
	      <form-submissions :identifier="selected" />
	    </q-tab-panel>
	  </q-tab-panels>
	</q-card>
      </div>
    </transition>
  </div>
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
      'tab': 'config',
    }
  },

  methods: {
    leaveForm () {
      this.selected = ''
      this.tab = 'config'
    }
  }
})
</script>
