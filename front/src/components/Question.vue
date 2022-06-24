<template>
  <v-app>
    <Header />
    <v-main>
      <NavHelpBar />
      <v-container>
        <v-card class="mt-12">
          <v-card-title>
            <span class="headline">質問フォーム</span>
          </v-card-title>

          <v-layout row fill-height justify-center align-center v-if="loading">
            <v-progress-circular :size="50" color="primary" indeterminate />
          </v-layout>

          <!-- 質門投稿フォーム -->
          <v-form v-else ref="form" v-model="valid" lazy-validation>
            <!--title-->
            <v-textarea v-model="credentials.question_title" label="質問タイトル" :rules="rules.question_title" required
              clearable clear-icon="mdi-close-circle" rows="1" outlined>
            </v-textarea>
            <!--content-->
            <v-textarea v-model="credentials.question_content" label="質問内容" :rules="rules.question_content" required
              clearable clear-icon="mdi-close-circle" auto-grow outlined>
            </v-textarea>
            <!--sorce code-->
            <v-textarea v-model="credentials.question_source_code" label="ソースコード" clearable
              clear-icon="mdi-close-circle" auto-grow outlined>
            </v-textarea>
            <v-dialog v-model="dialog" width="500">
              <template v-slot:activator="{ on, attrs }">
                <v-btn dark v-bind="attrs" v-on="on" :disabled="!valid">
                  質問する
                </v-btn>
              </template>

              <v-card>
                <v-card-title>
                  質問について
                </v-card-title>
                <v-card-text>
                  質問は削除できません．あとから編集することは可能です．
                  閲覧者が理解できる質問になっていますか？
                </v-card-text>
                <v-divider></v-divider>
                <v-card-actions>
                  <v-spacer></v-spacer>
                  <v-btn color="primary" @click="postQuestion">
                    質問を送信する
                  </v-btn>
                </v-card-actions>
              </v-card>
            </v-dialog>
          </v-form>
        </v-card>
      </v-container>
    </v-main>
  </v-app>
</template>
<script>
import { VueLoading } from 'vue-loading-template'
import Header from "../components/Header.vue";
import NavHelpBar from "../components/NavigationHelpBar.vue"
import Swal from "sweetalert2";
import header from "/src/node/axios";
import router from "../router";
import axios from "axios";

export default {
  components: {
    VueLoading,
    Header,
    NavHelpBar,
  },
  data() {
    return {
      loading: false,
      valid: true,
      credentials: {},
      rules: {
        question_title: [
          (v) => !!v || "質問タイトルは必須です",
        ],
        question_content: [
          (v) => !!v || "質問内容は必須です",
        ],
      },
      axios: {},
      dialog: false,
      userId: this.$session.get('user_id'),
      userObject: {},
      etherId: null,
    };
  },
  mounted() {
    this.checkToken();
    this.axiosHeader();
    this.getEtherId();
    this.getUserInfo();
  },
  methods: {
    checkToken() {
      this.$session.start();
      if (this.$session.has("token")) {
        console.log('Question.vue start user_id', this.$session.get('user_id'))
      }
      else {
        router.push("/signin");
      }
    },
    axiosHeader() {
      this.axios = header.setHeader();
    },
    //point追加機能を作成する
    postQuestion() {
      this.loading = true
      this.credentials["ether_id"] = this.etherId
      this.axios
        .post(process.env.VUE_APP_API_URL + "/app/create-question/", this.credentials)
        .then((res) => {
          console.log(res);
          this.loading = false
          //pointの追加
          this.putSendPoint()
          Swal.fire(
            'Goo job!',
            'success',
          )
          router.push('/')
        })
        .catch((e) => {
          this.loading = false;
          console.log(e);
          Swal.fire({
            icon: "warning",
            title: "Error",
            text: "入力が正しくありません",
            showConfirmButton: false,
            showCloseButton: false,
            timer: 3000,
          });
        });
      this.dialog = false
    },
    //現在obj空です
    createPutObject(){
       let obj ={
        "email":this.userObject.email,
        "password":this.userObject.password,
        "username":this.userObject.username,
        "status":this.userObject.status,
        "user_group":this.userObject.user_group,
        //所持ポイント増加
        "eth_stock":this.userObject.eth_stock + 1
      }
      console.log('Question.vue createPutObject() objの確認',obj)
      return obj
    },
    //質問したユーザーに対して，ポイントを送る
    putSendPoint(){
      let update_obj = this.createPutObject()
      console.log('Question.vue putSendPoint() obj', update_obj)
      this.axios
        .put(process.env.VUE_APP_API_URL + "/app/users/" + this.userId + "/", update_obj)
        .then((res) => {
          console.log(res);
        })
        .catch((e) => {
          console.log(e);
        });
    },
    sendEther() {
      this.loading = true
      send_object = this.userObject
      send_object.ether_stock = send_object.ether_stock + 1;
      console.log(ether_point)
      this.axios.put(process.env.VUE_APP_API_URL + "/app/users/" + this.userId, send_object)
        .then((res) => {
          console.log(res);
          this.loading = false
        })
        .catch((e) => {
          this.loading = false;
          console.log(e);
        });
    },
    getUserInfo() {
      axios
        .get(process.env.VUE_APP_API_URL + "/app/users/" + this.userId)
        .then((res) => {
          this.userObject = res.data
          console.log("Question.vue getUserInfo() userObject",res.data)
          this.createPutObject();
        })
        .catch((e) => {
          console.log(e);
        });
    },
    getEtherId() {
      this.axios
        .get(process.env.VUE_APP_API_URL + "/app/ether-get/" + this.userId)
        .then((res) => {
          let response = res.data[0]
          this.etherId = response["id"]
          console.log("QUestion.vue getEtherId() etherId", response["id"]);
        })
        .catch((e) => {
          console.log(e);
        });
    },
  }
}
</script>