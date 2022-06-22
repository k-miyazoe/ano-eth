<template>
  <v-app>
    <Header />
    <v-main>
      <v-container>
          <v-layout row fill-height justify-center align-center v-if="loading">
            <v-progress-circular :size="50" color="primary" indeterminate />
          </v-layout>
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
import { VueLoading } from 'vue-loading-template'
import Header from "../components/Header.vue";
import header from "/src/node/axios";
import router from "../router";

export default {
  components: {
    VueLoading,
    Header,
  },
  data() {
    return {
      loading: true,
      axios: {},
      userId: this.$session.get('user_id'),
      etherId: null,
      username: null,
    };
  },
  mounted() {
    this.checkToken();
    this.axiosHeader();
    //this.getEtherId();
  },
  methods: {
    //useridを取得
    checkToken() {
      this.$session.start();
      //tokenを所持しているなら
      if (this.$session.has("token")) {
        console.log('user_id', this.$session.get('user_id'))
        this.userId = this.$session.get('user_id')
        this.username = this.$session.get('user_name')
      }
      //所持していないなら
      else {
        router.push("/signin");
      }
    },
    axiosHeader() {
      this.axios = header.setHeader();
    },
    //グループによって，名前を空か空じゃないか変える
    initEtherObject() {
      let ether_obj = {
        user_id: this.user_id,
        user_name: this.username,
        ether_address: "",
        ether_password: "",
        ether_wallet: 0,
        ether_anonymous: false,
        ether_account_name: this.user_name,//usernameを取得する
      }
      console.log("init ether object", ether_obj)
      return ether_obj
    },
    //Etherモデルを作成
    createEtherUser() {
      let obj = initEtherObject()
      this.axios
        .post(process.env.VUE_APP_API_URL + "/app/create-ether/", obj)
        .then((res) => {
          console.log(res);
        })
        .catch((e) => {
          console.log(e);
        });
    },
  }
}
</script>