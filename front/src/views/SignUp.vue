<template>
  <v-app>
    <Header />
    <v-container grid-list-md>
      <v-layout row wrap align-center justify-center fill-height>
        <v-flex xs12 sm8 lg4 md5>
          <v-card class="mt-12">
            <v-card-title>
              <span class="headline">サインアップ</span>
            </v-card-title>

            <v-spacer />

            <v-card-text>
              <v-layout row fill-height justify-center align-center v-if="loading">
                <v-progress-circular :size="50" color="primary" indeterminate />
              </v-layout>

              <v-form v-else ref="form" v-model="valid" lazy-validation>
                <v-container>
                  <v-text-field v-model="credentials.email" label="学籍番号メールアドレス" :rules="rules.email" required />
                  <v-text-field type="password" v-model="credentials.password" :counter="20" label="パスワード"
                    :rules="rules.password" maxlength="20" required />
                  <!--確認用passoword-->
                  <v-text-field type="password" v-model="check_password" :counter="20" label="パスワード(確認用)"
                    :rules="rules.password" maxlength="20" required />
                  <v-text-field v-model="credentials.username" label="名前" :rules="rules.username" required />
                  <v-row>
                    <v-checkbox v-model="credentials.status" label="履修生" value="false" :rules="rules.status">
                    </v-checkbox>
                    <v-checkbox v-model="credentials.status" label="その他" value="true" :rules="rules.status">
                    </v-checkbox>
                  </v-row>
                </v-container>
                <v-btn class="pink white--text" :disabled="!valid" @click="signUp">
                  サインアップ
                </v-btn>
              </v-form>
            </v-card-text>
          </v-card>
          <router-link to='/signin'>
            アカウントがある方はこちらから
          </router-link>
        </v-flex>
      </v-layout>
    </v-container>
  </v-app>
</template>

<script>
import Swal from "sweetalert2";
import router from "../router";
import header from "/src/node/axios";
import Header from "../components/Header.vue";

export default {
  components: {
    Header,
  },
  data: () => ({
    credentials: {},
    axios: {},
    valid: true,
    loading: false,
    check_password: "",
    rules: {
      email: [
        (v) => !!v || "メールアドレスは必須です",
      ],
      password: [
        (v) => !!v || "パスワードは必須です",
        (v) =>
          (v && v.length > 7) || "パスワードは8文字以上でなければなりません",
      ],
      username: [
        (v) => !!v || "名前は必須です",
      ],
      status: [
        (v) => !!v || "選択は必須です",
      ]
    },
    //履修生(false) 先生,TA(true)
    status: null,
  }),
  mounted() {
    //this.checkToken();
    this.axiosHeader()
  },
  methods: {
    signUp() {
      if (this.$refs.form.validate()) {
        this.loading = true;
        console.log(this.credentials)
        //パスワードの確認
        if (this.checkPassword(this.credentials.password, this.check_password)) {
          this.axios
            .post(process.env.VUE_APP_API_URL + "/app/create-user/", this.credentials)
            .then((res) => {
              console.log(res);
              router.push("/");
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
        }
        else {
          Swal.fire({
            icon: "warning",
            title: "Error",
            text: "パスワードが一致しません",
            showConfirmButton: false,
            showCloseButton: false,
            timer: 1000,
          });
          this.loading = false;
          this.credentials.password = "",
            this.check_password = ""
        }
      }
    },
    checkToken() {
      this.$session.start();
      if (this.$session.has("token")) {
        router.push("/");
      }
    },
    checkPassword(pass1, pass2) {
      if (pass1 == pass2) {
        return true
      } else {
        return false
      }
    },
    axiosHeader() {
      this.axios = header.setHeader();
    },
    test_log() {
      console.log(process.env.VUE_APP_API_URL + "/app/create-user/")
      //console.log(this.checkPassword(this.credentials.password,this.check_password))
      //router.push("/");
    },
  },
};
</script>