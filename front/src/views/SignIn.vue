<template>
  <v-app>
    <Header />
    <v-container grid-list-md>
      <v-layout row wrap align-center justify-center fill-height>
        <v-flex xs12 sm8 lg4 md5>
          <v-card class="mt-12">
            <v-card-title>
              <span class="headline">サインイン</span>
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
                    :rules="rules.password" maxlength="20" required v-on:keydown.enter="signIn" />
                </v-container>
                <v-btn class="pink white--text" :disabled="!valid" @click="signIn">
                  サインイン
                </v-btn>
              </v-form>
            </v-card-text>
          </v-card>
          <router-link to='/signup'>
            アカウントを登録していない方はこちらから
          </router-link>
        </v-flex>
      </v-layout>
    </v-container>
  </v-app>
</template>

<script>
import axios from "axios";
import Swal from "sweetalert2";
import router from "../router";
import Header from "../components/Header.vue";
export default {
  components: {
    Header,
  },
  data: () => ({
    credentials: {},
    valid: true,
    loading: false,
    rules: {
      email: [
        (v) => !!v || "メールアドレスは必須です",
      ],
      password: [
        (v) => !!v || "パスワードは必須です",
        (v) =>
          (v && v.length > 7) || "パスワードは8文字以上でなければなりません",
      ],
    },
  }),
  mounted() {
    this.checkToken();
  },
  methods: {
    signIn() {
      if (this.$refs.form.validate()) {
        this.loading = true;
        axios
          .post(process.env.VUE_APP_API_URL + "/auth/", this.credentials)
          .then((res) => {
            this.$session.start();
            this.$session.set("token", res.data.token);
            this.$session.set('user_id', res.data.user_id);
            console.log(res);
            router.push("/");
          })
          .catch((e) => {
            this.loading = false;
            console.log(e);
            Swal.fire({
              icon: "warning",
              title: "Error",
              text: "メールアドレスもしくはパスワード、または両方が間違っています",
              showConfirmButton: false,
              showCloseButton: false,
              timer: 3000,
            });
          });
      }
    },
    checkToken() {
      this.$session.start();
      if (this.$session.has("token")) {
        router.push("/");
      }
    },
    //mailアドレスからuseridを取得する
    getUserId() {
      axios.post(process.env.VUE_APP_API_URL + "/app/user/")
        .then((res) => {
          console.log(res);
        })
        .catch((e) => {
          console.log(e)
        })
    }
  },
};
</script>