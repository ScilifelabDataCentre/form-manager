<template>
  <q-dialog v-model="showDialog">
    <q-card>
      <q-card-section class="row items-center">
        <q-avatar icon="delete" text-color="negative" />
        <span class="q-ml-sm">Are you sure you want to delete this {{ entryType }}?</span>
      </q-card-section>
      
      <q-card-actions align="right">
        <q-btn
	  v-close-popup
	  flat
          label="Delete"
          color="negative"
	  class="confirm-delete"
          @click="confirmDelete" />
        <q-btn
	  v-close-popup
	  flat
	  label="Cancel"
	  color="grey-7" />
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>

<script>
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'DeleteDialog',
  
  props: {
    modelValue: {  // show
      type: Boolean,
      required: true,
    },
    entryType: {
      type: String,
      default: "form",
    }
  },

  emits: ['update:modelValue', 'delete-confirmed'],

  computed: {
    showDialog: {
      get () {
	return this.modelValue
      },
      set (newValue) {
	this.$emit('update:modelValue', newValue)
      }
    }
  },

  methods: {
    confirmDelete() {
      this.$emit('delete-confirmed');
    },
  },
})
</script>
