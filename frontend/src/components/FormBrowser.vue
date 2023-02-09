<template>
  <q-table
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
      <q-input
	v-model="filter"
	rounded
	outlined
	dense
	debounce="300"
	placeholder="Search">
        <template #append>
          <q-icon name="search" />
        </template>
      </q-input>
    </template>
    <template #body="props">
      <q-tr :props="props" @click=selectForm(props)>
        <q-td key="title" :props="props">
          {{ props.row.title }}
        </q-td>
        <q-td key="identifier" :props="props">
          {{ props.row.identifier }}
        </q-td>
        <q-td key="recaptcha" :props="props">
          <q-icon
	    :name="props.row.recaptcha ? 'check_circle' : 'cancel'"
	    :color="props.row.recaptcha ? 'positive' : 'negative'"
	    size="1.5em">
          </q-icon>
        </q-td>
        <q-td key="sendEmail" :props="props">
          <q-icon
	    :name="props.row.email ? 'check_circle' : 'cancel'"
	    :color="props.row.email ? 'accent' : 'secondary'"
	    size="1.5em">
          </q-icon>
        </q-td>
        <q-td key="redirect" :props="props">
          <q-icon
	    :name="props.row.redirect ? 'check_circle' : 'cancel'"
	    :color="props.row.redirect ? 'accent' : 'secondary'"
	    size="1.5em">
          </q-icon>
        </q-td>
      </q-tr>
    </template>
  </q-table>
</template>

<script>
import { defineComponent } from 'vue'

import StringListEditor from 'components/StringListEditor.vue'

export default defineComponent({
  name: 'FormBrowser',

  props: {
    modelValue: {
      type: String,
      required: true,
    },
    refreshNeeded: {
      type: Boolean,
      default: false,
    },
  },

  emits: ['update:modelValue', 'refresh-done'],

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

  watch: {
    refreshNeeded (newValue) {
      if (newValue === true) {
	this.getEntries();
      }
    },
  },

  mounted () {
    this.getEntries();
  },

  methods: {
    getEntries () {
      this.loading = true;
      this.$api
	.get('/form')
        .then((response) => {
	  this.entries = response.data['forms']
	})
      .catch((err) => {
	this.loadError = true;
      })
	.finally(() => {
	  this.loading = false
	  this.$emit('refresh-done')
	});
    },
    selectForm(props) {
      this.$emit('update:modelValue', props.row.identifier);
    },
  },
})
</script>
