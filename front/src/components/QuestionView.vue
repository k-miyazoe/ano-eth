<template>
    <v-app>
        <Header />
        <v-main>
            <NavHelpBar />
            <v-container fluid>
                <!--質問詳細-->
                <v-card class="mx-auto" max-height="344">
                    <v-col class="mb-10">
                        <v-card-title>{{ one_quesiton.question_title }}</v-card-title>
                        <v-card-text>{{ one_quesiton.question_content }}</v-card-text>
                        <v-card-text>{{ one_quesiton.question_source_code }}</v-card-text>
                        <v-card-actions>
                            <v-btn color="orange" text>
                                高評価
                            </v-btn>
                        </v-card-actions>
                    </v-col>
                </v-card>
                <!--回答一覧-->
                <v-card v-for="item in any_answer" :key="item.id">
                    <v-card-title>回答 </v-card-title>
                    <v-card-text>{{ item.answer_content }}</v-card-text>
                    <v-card-text>{{ item.answer_source_code }}</v-card-text>
                    <v-card-actions>
                        <v-btn color="orange" text>
                            高評価
                        </v-btn>
                    </v-card-actions>
                </v-card>
                <!--回答フォーム-->
                <v-card class="mt-10">
                    <v-card-title>
                        回答フォーム
                    </v-card-title>
                    <v-form ref="form" v-model="valid" lazy-validation>
                        <v-textarea v-model="credentials.answer_content" label="解決策・提案" :rules="rules.answer_content"
                            clearable clear-icon="mdi-close-circle" auto-grow outlined>
                        </v-textarea>
                        <v-textarea v-model="credentials.answer_source_code" label="ソースコード" clearable
                            clear-icon="mdi-close-circle" auto-grow outlined>
                        </v-textarea>
                    </v-form>
                    <!--回答送信ボタン-->
                    <v-dialog v-model="dialog" width="500">
                        <template v-slot:activator="{ on, attrs }">
                            <v-btn dark v-bind="attrs" v-on="on" :disabled="!valid">
                                回答する
                            </v-btn>
                        </template>

                        <v-card>
                            <v-card-title>
                                回答について
                            </v-card-title>
                            <v-card-text>
                                回答は削除できません．あとから編集することは可能です．
                                質問者が理解できる回答になっていますか？
                            </v-card-text>
                            <v-divider></v-divider>
                            <v-card-actions>
                                <v-spacer></v-spacer>
                                <v-btn color="primary" @click="postAnswer">
                                    回答を送信する
                                </v-btn>
                            </v-card-actions>
                        </v-card>
                    </v-dialog>

                </v-card>
            </v-container>
        </v-main>
    </v-app>
</template>

<script>
import Header from "../components/Header.vue";
import NavHelpBar from "../components/NavigationHelpBar.vue"
import axios from "axios";
import header from "/src/node/axios";
import router from "../router";

export default {
    components: {
        Header,
        NavHelpBar
    },
    data() {
        return {
            one_quesiton: {},
            any_answer: {},
            id: this.$route.params.id,
            question_id: null,
            dialog: false,
            axios: {},
            userId: this.$session.get('user_id'),
            userObject: {},
            etherId: null,
            credentials: {},
            rules: {
                answer_content: [
                    (v) => !!v || "回答内容は必須です",
                ],
            },
            valid: true,
            loading: false,
        };
    },
    mounted() {
        this.checkToken()
        this.getUserInfo()
        this.getEtherId()
        this.axiosHeader()
        //質問内容とと質問idを取得
        this.getOneQuestion()
        this.getAnyAnswer()
    },
    methods: {
        checkToken() {
            this.$session.start();
            //tokenを所持しているなら
            if (this.$session.has("token")) {
                console.log('user_id', this.$session.get('user_id'))
            }
            //所持していないなら
            else {
                router.push("/signin");
            }
        },
        getOneQuestion() {
            axios
                .get(process.env.VUE_APP_API_URL + "/app/get-question/" + this.id)
                .then((res) => {
                    this.one_quesiton = res.data
                    this.question_id = this.one_quesiton.id
                })
                .catch((e) => {
                    console.log(e);
                });
        },
        getAnyAnswer() {
            axios
                .get(process.env.VUE_APP_API_URL + "/app/get-answer/" + this.id + '/')
                .then((res) => {
                    console.log(res.data);
                    this.any_answer = res.data
                })
                .catch((e) => {
                    console.log(e);
                });
        },
        postAnswer() {
            this.loading = true
            this.credentials["ether_id"] = this.etherId
            this.credentials["question_id"] = this.question_id
            this.axios
                .post(process.env.VUE_APP_API_URL + "/app/create-answer/", this.credentials)
                .then((res) => {
                    console.log(res);
                    this.loading = false
                    this.credentials = {}
                    //point追加
                    this.putSendPoint()
                    this.getAnyAnswer()
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
        axiosHeader() {
            this.axios = header.setHeader();
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
                    console.log(res.data)
                    this.createPutObject()
                })
                .catch((e) => {
                    console.log(e);
                });
        },
        getEtherId() {
            console.log(process.env.VUE_APP_API_URL + "/app/ether-get/" + this.userId + "/")
            axios
                .get(process.env.VUE_APP_API_URL + "/app/ether-get/" + this.userId)
                .then((res) => {
                    let data = res.data[0]
                    console.log("EtherId", data["id"]);
                    this.etherId = data["id"]
                })
                .catch((e) => {
                    console.log(e);
                });
        },

        //pointを与える処理
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
            console.log('QuestionView.vue createPutObject() objの確認',obj)
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
        log() {
            console.log(this.userId, this.etherId, this.question_id, this.credentials)
            this.credentials = {}
            this.getAnyAnswer()
        }
    },
}
</script>