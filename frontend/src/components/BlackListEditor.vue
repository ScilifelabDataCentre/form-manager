<template>
<q-list
  bordered
  separator
  >
  <q-item>
    <q-item-section>
      <q-item-label>Blacklist rules</q-item-label>
      <q-item-label caption>A submission will be blacklisted if it matches all rules in any of the rule groups.</q-item-label>
    </q-item-section>
  </q-item>
  <q-expansion-item
    v-for="ruleGroup, i in blacklist"
    :key="i"
    :label="'Rule group ' + (i+1)"
    >
    <q-list>
      <q-item>
	<q-item-section>
	  <q-item-label>Rules</q-item-label>
	  <q-item-label caption>Each rule is a regular expression used to evaluate the value from the corresponding key in the submission.</q-item-label>
	</q-item-section>
      </q-item>
      <q-item
	v-for="value, key in ruleGroup"
	  :key="key">
	<q-item-section>
	  <q-input
	    v-model="ruleGroup[key]"
	    outlined
	    hide-bottom-space
	    :label="key">
	    <template #after>
	      <q-btn
		icon="delete"
		dense
		square
		size="md"
		color="negative"
		@click="deleteRule(i, key)" />
	    </template>
	  </q-input>
	</q-item-section>
      </q-item>
      <q-item
	v-ripple
	clickable
	>
	<q-item-section avatar>
	  <q-icon color="positive" name="add" />
	</q-item-section>
	<q-item-section>
	  Add rule
	</q-item-section>
      </q-item>
      <q-item>
	<q-item-section class="flex">
	  <q-input
	    flat
	    icon="add"
	    label="Key to add a rule for"
	    color="positive"
	    class="col-shrink"
	    @click="addRule(i, key)" />
	</q-item-section>
      </q-item>
    </q-list>
  </q-expansion-item>
  
  <q-item
    v-ripple
    clickable
    @click="addRuleGroup"
    >
    <q-item-section avatar>
      <q-icon color="positive" name="add" />
    </q-item-section>
    <q-item-section>
      Add rule group
    </q-item-section>
  </q-item>
</q-list>
</template>

<script>

export default {
  name: 'BlacklistEditor',

  props: {
    modelValue: {
      type: Array,
      required: true,
    },
  },

  emits: ['update:modelValue'],

  data () {
    return {
      newValue: '',
      newRules: [],
      valueExistsError: false,
      blacklist: [
	{
	  key: "value",
	  anotherKey: "AnotherValue"
	},
	{
	  key: "value2",
	  anotherKey: "AnotherValue2"
	},
      ],
    }
  },

  computed: {
    enableAdd: {
      get () {
        return this.evaluateValue(this.newValue);
      },
    },
  },

  watch: {
    blacklist (newVal): {
      
    }
  },

  methods: {
    addRuleGroup() {
      this.blacklist.push({})
      this.newRules.push[]
    },

    addRule(i, key) {
      this.blacklist[i].hasOwnProperty('key')
      this.blacklist[i][key] = ""
    },

    deleteRule(i, key) {
      delete this.blacklist[i].append({})
      this.newRules.splice(i, 1)
    },
    
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
