<template>
<div>
  <div>
    <q-input
      v-model="newValue"
      dense
      stack-label
      hide-bottom-space
      outlined
      :label="fieldTitle"
      :rules="[ function (val) { return (evaluateValue(val) || val.length === 0) || 'No whitespace at beginning nor end and must not already exist.' }]">
      @keyup.enter="addValue"
      <template #after>
        <q-btn
	  icon="add"
          dense
          size="md"
          :disabled="!enableAdd"
          color="positive"
          @click="addValue" />
      </template>
    </q-input>
    <div class="flex">
      <q-chip
	v-for="value of modelValue"
	:key="value"
	square
	:removable="(staticCurrentUser && currentUser === value) ? false : true"
	color="primary"
	text-color="white"
	@remove="deleteValue(value)">
	{{ value }}
      </q-chip>
    </div>
  </div>
</div>
</template>

<script>
import { useUserStore } from 'stores/user'

export default {
  name: 'StringListEditor',

  props: {
    staticCurrentUser: {
      type: Boolean,
      default: false,
    },
    modelValue: {
      type: Array,
      required: true,
    },

    fieldTitle: {
      type: String,
      required: true,
    },
  },

  emits: ['update:modelValue'],

  data () {
    return {
      newValue: '',
      valueExistsError: false,
    }
  },

  computed: {
    enableAdd: {
      get () {
        return this.evaluateValue(this.newValue);
      },
    },
    currentUser: {
      get () {
	const store = useUserStore();
	return store.email
      }
    },
  },

  methods: {
    evaluateValue (val) {
      return (val.trim() === val && !this.modelValue.includes(this.newValue));
    },

    addValue() {
      if (this.enableAdd) {
        this.valueExistsError = false;
        if (!this.modelValue.includes(this.newValue)) {
          this.$emit('update:modelValue', this.modelValue.concat(this.newValue))
          this.newValue = '';
        }
        else
          this.valueExistsError = true;
      }
    },

    deleteValue(value) {
      this.$emit('update:modelValue', this.modelValue.filter((entry) => entry !== value))
    },
  },
}
</script>
