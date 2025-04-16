<template>
  <div class="fullscreen text-primary text-center q-pa-md flex flex-center">
    <div>
      <div class="text-h2">
        {{ postResponse }}
      </div>

      <q-btn
        v-if="redirect"
        label="Continue"
        icon-right="arrow_forward"
        class="q-my-lg"
        color="primary"
        type="a"
        :href="redirect"
      />
    </div>
  </div>
</template>

<script>
import { defineComponent } from "vue";
import axios from "axios";
import { copyToClipboard } from "quasar";

export default defineComponent({
  name: "FormPostResult",

  data() {
    return {
      postResponse: "",
      redirect: "",
      progress: 0,
    };
  },

  mounted() {
    if (this.$route.path === "/success")
      this.postResponse = "Form successfully submitted!";
    else this.postResponse = "Form submission failed!";
    this.redirect = this.$route.query.redirect;
  },
});
</script>
