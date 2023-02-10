<template>
<transition
  appear
  enter-active-class="animated fadeIn"
  leave-active-class="animated fadeOut"
  >
  <q-banner
    v-show="show"
    class="fixed-bottom bg-primary text-white"
    >
    <template #avatar>
      <q-icon name="cookie" color="white" />
    </template>
    {{ note }}
    <template #action>
      <q-btn flat color="white" label="Ok" @click="accepted" />
    </template>
  </q-banner>
</transition>
</template>

<script>
import { useQuasar } from 'quasar'
import { defineComponent, ref, toRef, onMounted } from 'vue'

export default defineComponent({
name: 'CookieNotifier',
  props: {
    note: {
      type: String,
      default: 'This system uses cookies to manage your session.',
    },
  },

  setup(props) {
    const $q = useQuasar()
    const show = ref(false)

    const accepted = () => {
      $q.cookies.set('cookie_ok', true)
      show.value = false
    }

    onMounted(() => {
      const value = $q.cookies.get('cookie_ok')
      if (value !== 'true') {
	show.value = true
      }
    })

    return { show, accepted }
  },
})
</script>
