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
import axios from "axios";
import Swal from "sweetalert2";


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
      user_group: null,
      ether_user_name: null,
      ether_obj: null,
    };
  },
  created() {
    this.checkToken();
    this.axiosHeader();
  },
  mounted() {
    this.getUserGroup()
  },
  methods: {
    checkToken() {
      console.log('Create Ether start 1')
      this.$session.start();
      //tokenを所持しているなら
      if (this.$session.has("token")) {
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
    //groupを取得する
    getUserGroup() {
      axios
        .get(process.env.VUE_APP_API_URL + "/app/users/" + this.userId + "/")
        .then((res) => {
          this.user_group = res.data.user_group
          this.checkUserName()
          this.initEtherObject()
          this.createEtherUser()
        })
        .catch((e) => {
          console.log(e);
        });
    },
    //groupを判断し，usernameを返す
    checkUserName(){
      console.log("1 checkUserName start")
      if(this.user_group == "A"){
        this.ether_user_name = this.username
      } else {
        this.ether_user_name = "匿名"
      }
    },
    //モデルのobjデータ生成
    initEtherObject() {
      console.log('2 initEtherObject start')
      let ether_obj = {
        user_id: this.userId,
        //質問・回答の際表示される名前
        user_name: this.ether_user_name,
        ether_wallet: 0,
        ether_anonymous: false,
        ether_account_name: this.username,//usernameを取得する
      }
      console.log("init ether object ", ether_obj)
      this.ether_obj = ether_obj
    },
    //Etherモデルを作成
    createEtherUser() {
      console.log('3 createEtherUser start')
      this.axios
        .post(process.env.VUE_APP_API_URL + "/app/create-ether/",this.ether_obj)
        .then((res) => {
          Swal.fire(
            'signin success!',
            'success',
          )
          router.push('/')
        })
        .catch((e) => {
          console.log(e);
        });
    },
  }
}
</script>