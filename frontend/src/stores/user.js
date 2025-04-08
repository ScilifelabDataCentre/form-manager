import { defineStore } from "pinia";
import axios from "axios";

export const useUserStore = defineStore("user", {
  state: () => ({
    email: "",
    loaded: false,
  }),
  actions: {
    getUserInfo() {
      return new Promise((resolve, reject) => {
        this.loaded = false;
        axios
          .get("/api/v1/user/me")
          .then((response) => {
            this.email = response.data["user"];
            this.loaded = true;
            resolve();
          })
          .catch(() => {
            this.email = "";
            this.loaded = true;
            reject();
          });
      });
    },
  },
});
