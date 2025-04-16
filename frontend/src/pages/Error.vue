<template>
  <div
    class="fullscreen bg-primary text-white text-center q-pa-md flex flex-center"
  >
    <div>
      <div style="font-size: 30vh">Error</div>

      <div class="text-h2" style="opacity: 0.4">
        {{ message }}
      </div>
    </div>
  </div>
</template>

<script>
import { defineComponent } from "vue";
import axios from "axios";

export default defineComponent({
  name: "ErrorPage",
  props: {
    message: {
      type: String,
      default: "Something went wrong",
    },
  },
});
</script>
