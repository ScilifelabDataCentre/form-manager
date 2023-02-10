<template>
  <q-layout view="lHh Lpr lFf">
    <q-header elevated>
      <q-toolbar>
        <q-toolbar-title>
          Form Manager
        </q-toolbar-title>

	<div class="q-mr-xl text-weight-bold text-caption">
	  {{ version }}
	</div>
        <q-btn
	  v-if="userStore.email !== ''"
	  flat
	  round
	  type="a"
	  href="/api/v1/user/logout"
	  icon="logout"
	  />
      </q-toolbar>
    </q-header>

    <q-page-container>
      <router-view />
    </q-page-container>
    <cookie-notifier />
  </q-layout>
</template>

<script>
import { defineComponent, ref } from 'vue'
import { useUserStore } from 'stores/user'
import CookieNotifier from 'components/CookieNotifier.vue'

export default defineComponent({
  name: 'MainLayout',

  components: {
    'cookie-notifier': CookieNotifier,
  },
  
  setup() {
    const userStore = useUserStore()
    const version = process.env.VERSION

    return { userStore, version }
  },
})
</script>
