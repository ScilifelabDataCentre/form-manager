<template>
  <q-page class="flex flex-center">
    <q-btn
      label="Login"
      icon="login"
      type="a"
      href="/api/v1/user/login"
      text-color="white"
      color="primary"
      class="q-pa-lg"
    />
  </q-page>
</template>

<script>
import { defineComponent } from "vue";

export default defineComponent({
  name: "IndexPage",
});
</script>
