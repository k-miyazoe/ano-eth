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
    };
  },
  created() {
    this.checkToken();
    this.axiosHeader();
  },
  mounted() {
    this.createEtherUser();
  },
  methods: {
    checkToken() {
      console.log('Create Ether start 1')
      this.$session.start();
      //tokenを所持しているなら
      if (this.$session.has("token")) {
        this.userId = this.$session.get('user_id')
        this.username = this.$session.get('user_name')
        console.log('user_id:', this.$session.get('user_id'))
        console.log('user_name:', this.username)
      }
      //所持していないなら
      else {
        router.push("/signin");
      }
    },
    axiosHeader() {
      this.axios = header.setHeader();
    },
    getUserGroup() {
      console.log('Get user group start 4.1')
      axios
        .get(process.env.VUE_APP_API_URL + "/app/users/" + this.userId + "/")
        .then((res) => {
          console.log("user_group:", res.data.user_group);
          let user_group = res.data.user_group
          return user_group
        })
        .catch((e) => {
          console.log(e);
          return false;
        });
    },
    //usernameがない
    initEtherObject() {
      let name = "匿名"
      let group = this.getUserGroup()
      //Aなら実名、それ以外なら匿名
      if (group == "A") {
        name = this.user_name
      }

      let ether_obj = {
        user_id: this.userId,
        user_name: name,
        ether_wallet: 0,
        ether_anonymous: false,
        ether_account_name: this.username,//usernameを取得する
      }
      console.log("init ether object done 4.2", ether_obj)
      return ether_obj
    },
    //Etherモデルを作成
    createEtherUser() {
      console.log('createEtherUser start 2')
      //let obj = this.initEtherObject()
      console.log('post api start 3')
      this.axios
        .post(process.env.VUE_APP_API_URL + "/app/create-ether/", this.initEtherObject())
        .then((res) => {
          console.log("create ether success", res);
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