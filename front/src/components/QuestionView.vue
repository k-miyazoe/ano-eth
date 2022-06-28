<template>
    <v-app>
        <Header />
        <v-main>
            <NavHelpBar />
            <v-container fluid>
            <v-btn color="primary" @click="log">
            log button
            </v-btn>
                <!--質問詳細-->
                <v-card class="mx-auto" max-height="344">
                    <v-col class="mb-10">
                        <v-card-title>{{ one_quesiton.question_title }}</v-card-title>

                        <v-card>
                            <v-card-text>内容</v-card-text>
                            <v-card-text>{{ one_quesiton.question_content }}</v-card-text>
                        </v-card>

                        <v-card>
                            <v-card-text>ソースコード</v-card-text>
                            <v-card-text>{{ one_quesiton.question_source_code }}</v-card-text>
                        </v-card>

                        <v-card-actions>
                            <v-btn color="orange" text @click="highlyRatedQuestion">
                                高評価
                            </v-btn>
                            <!--解決-->
                            <v-dialog v-model="dialog" width="500">
                             <template v-slot:activator="{ on, attrs }">
                              <v-btn color="green" text v-bind="attrs" v-on="on" :disabled="!valid">
                                解決
                              </v-btn>
                             </template>
                             <v-card>
                              <v-card-title>
                                質問について
                              </v-card-title>
                              <v-card-text>
                                質問が解決されましたか？
                              </v-card-text>
                              <v-divider></v-divider>
                              <v-card-actions>
                                <v-spacer></v-spacer>
                                <v-btn color="green" text @click="resolvedQuestion">
                                    解決する
                                </v-btn>
                              </v-card-actions>
                             </v-card>
                            </v-dialog>


                        </v-card-actions>
                    </v-col>
                </v-card>

                <!--回答一覧-->
                <v-card v-for="(item,index) in any_answer" :key="index">
                    <v-card-title>回答 {{index + 1}}</v-card-title>
                    <v-card-text>{{ item.answer_content }}</v-card-text>
                    <v-card-text>{{ item.answer_source_code }}</v-card-text>
                    <v-card-actions>
                        <v-btn color="orange" text @click="highlyRatedAnswer">
                            高評価
                        </v-btn>

                        <!--ベストアンサー-->
                         <v-dialog v-model="dialog" width="500">
                          <template v-slot:activator="{ on, attrs }">
                            <v-btn color="red" text v-bind="attrs" v-on="on" :disabled="!valid">
                              ベストアンサー
                            </v-btn>
                          </template>

                          <v-card>
                            <v-card-title>
                                ベストアンサーについて
                            </v-card-title>
                            <v-card-text>
                               ベストアンサーを決定しますか？
                            </v-card-text>
                            <v-divider></v-divider>
                            <v-card-actions>
                                <v-spacer></v-spacer>
                                <v-btn color="red" @click="bestAnswer(index)">
                                    決定する
                                </v-btn>
                            </v-card-actions>
                           </v-card>
                          </v-dialog>
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
import Swal from "sweetalert2";

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
            question_ether_id: 0,
            ether_user_name: "",
            best_answer_has: false,
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
        //前処理
        checkToken() {
            this.$session.start();
            //tokenを所持しているなら
            if (this.$session.has("token")) {
               console.log('now user_id', this.$session.get('user_id'))
            }
            //所持していないなら
            else {
                router.push("/signin");
            }
        },
        axiosHeader() {
            this.axios = header.setHeader();
        },
        //質問の高評価や解決処理との依存関係
        getOneQuestion() {
            axios
                .get(process.env.VUE_APP_API_URL + "/app/get-question/" + this.id)
                .then((res) => {
                    this.one_quesiton = res.data
                    this.question_id = this.one_quesiton.id
                    //logは表示される
                    console.log('one_question.ether_id:', this.one_quesiton.ether_id)
                    //TypeErrorはここが原因
                    //this.question_ether_id = this.one_question.ether_id
                })
                .catch((e) => {
                    console.log(e);
                });
        },
        //回答高評価との依存関係
        getAnyAnswer() {
            axios
                .get(process.env.VUE_APP_API_URL + "/app/get-answer/" + this.id + '/')
                .then((res) => {
                    console.log(res.data);
                    this.any_answer = res.data
                    //
                    this.hasBestAnswer(res.data)
                })
                .catch((e) => {
                    console.log(e);
                });
        },
        getUserInfo() {
            axios
                .get(process.env.VUE_APP_API_URL + "/app/users/" + this.userId)
                .then((res) => {
                    this.userObject = res.data
                    //console.log(res.data)
                    this.createPutObject()
                })
                .catch((e) => {
                    console.log(e);
                });
        },
        //useridからetherid,usernameを取得する/
        //現在ログインしているユーザーのether_idを取得する
        getEtherId() {
            axios
                .get(process.env.VUE_APP_API_URL + "/app/ether-get/" + this.userId)
                .then((res) => {
                    let data = res.data[0]
                    this.etherId = data["id"]
                    this.ether_user_name = data["user_name"]
                })
                .catch((e) => {
                    console.log(e);
                });
        },

        //イベント処理
        postAnswer() {
            this.loading = true
            this.credentials["ether_id"] = this.etherId
            this.credentials["question_id"] = this.question_id
            this.axios
                .post(process.env.VUE_APP_API_URL + "/app/create-answer/", this.credentials)
                .then((res) => {
                    //console.log(res);
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
        sendEther() {
            this.loading = true
            send_object = this.userObject
            send_object.ether_stock = send_object.ether_stock + 1;
            //console.log(ether_point)
            this.axios.put(process.env.VUE_APP_API_URL + "/app/users/" + this.userId, send_object)
                .then((res) => {
                    //console.log(res);
                    this.loading = false
                })
                .catch((e) => {
                    this.loading = false;
                    console.log(e);
                });
        },

        //pointを与える処理
        //swith文でuser,ether,questionのオブジェクトをそれぞれ引数から作れるようにしたい
        createPutObject() {
            let obj = {
                "email": this.userObject.email,
                "password": this.userObject.password,
                //所持ポイント増加
                "eth_stock": this.userObject.eth_stock + 1
            }
            //console.log('QuestionView.vue createPutObject() objの確認', obj)
            return obj
        },
        //質問したユーザーに対して，ポイントを送る[高評価を受けた場合]
        putSendPoint() {
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

        //高評価　質問 　useridなどがまだ未定
        highlyRatedQuestion() {
            //etherとquestionのputを行う userはMypageの際に更新する

            let ether_update_obj = {
                user_id: null,
                eth_wallet: null//this.eth_wallet + 1
            }
            //質問のether_id -> なぞにether_id取得できない問題にあたる
            this.axios
                .put(process.env.VUE_APP_API_URL + "/app/ether-update/" + this.userId + "/", ether_update_obj)
                .then((res) => {
                    console.log(res);
                })
                .catch((e) => {
                    console.log(e);
                });


            //質問 update function 質問の評価値を1上げる
            let question_update_obj = {
                ether_id: this.one_quesiton.ether_id,
                question_value: this.one_question.question_value + 1
            }

            this.axios
                .put(process.env.VUE_APP_API_URL + "/app/update-question/" + this.question_id + "/", question_update_obj)
                .then((res) => {
                    console.log(res);
                    console.log('質問の評価値up')
                })
                .catch((e) => {
                    console.log(e);
                });

        },
        //質問解決 コード終了
        resolvedQuestion() {
            if (this.hasBestAnswer()) {
                //質問解決処理 押し間違えても大丈夫か[現在こっち]または二段階質問にするか
                let resolve_obj = {
                    ether_id: this.one_quesiton.ether_id,
                    //booleanを逆にする
                    question_status: !this.one_quesiton.question_status
                }
                this.axios
                    .put(process.env.VUE_APP_API_URL + "/app/update-question/" + this.question_id + "/", resolve_obj)
                    .then((res) => {
                        console.log(res);
                        Swal.fire(
                            '質問が解決されました!',
                            'success',
                        )
                    })
                    .catch((e) => {
                        console.log(e);
                    });

                console.log('質問解決')
            } else {
                Swal.fire({
                    icon: "warning",
                    title: "Error",
                    text: "ベストアンサーがありません．ベストアンサーを選択してください",
                    showConfirmButton: false,
                    showCloseButton: false,
                    timer: 3000,
                });
            }
        },
        //高評価  回答 objの中身が未定
        //フロントからpkなどを引数でもらっていく
        highlyRatedAnswer() {
            let ether_update_obj = {
                user_id: null,
                eth_wallet: null//this.eth_wallet + 1
            }
            this.axios
                .put(process.env.VUE_APP_API_URL + "/app/ether-update/" + this.userId + "/", ether_update_obj)
                .then((res) => {
                    console.log(res);
                })
                .catch((e) => {
                    console.log(e);
                });


            //回答の評価値を1上げる 回答した人のetheridが必要
            let answer_update_obj = {
                ether_id: null,
                answer_value: 1
            }

            this.axios
                //answer_idが必要
                .put(process.env.VUE_APP_API_URL + "/app/update-answer/" + this.question_id + "/", answer_update_obj)
                .then((res) => {
                    console.log(res);
                    console.log('質問の評価値up')
                })
                .catch((e) => {
                    console.log(e);
                });


            console.log('高評価　質問')
        },
        //質問者が回答に対してベストアンサーを決める[一旦ok]
        bestAnswer(answer_list_index) {
            //複数のベストアンサーは選べない
            if(this.best_answer_has){
              Swal.fire({
              icon: "warning",
              title: "Error",
              text: "すでにベストアンサーは存在しています！",
              showConfirmButton: false,
              showCloseButton: false,
              timer: 3000,
            });
            }
            //ベストアンサー決定
            if (this.etherId == this.one_quesiton.ether_id) {
                let answer_update_obj = {
                    ether_id: this.any_answer[answer_list_index].ether_id,
                    question_id: this.question_id,
                    answer_best: true
                }
                let answer_url = this.any_answer[answer_list_index].id
                //this.question_id -> answerのpkを指定する
                this.axios
                    .put(process.env.VUE_APP_API_URL + "/app/update-answer/" + answer_url + "/", answer_update_obj)
                    .then((res) => {
                        console.log(res);
                        Swal.fire(
                            'ベストアンサーを決定しました!',
                            'success',
                        )
                    })
                    .catch((e) => {
                        console.log(e);
                    });

            } 
            //質問者でないユーザーはできない
            else {
                Swal.fire({
                    icon: "warning",
                    title: "Error",
                    text: "質問者のみベストアンサーを決めることができます",
                    showConfirmButton: false,
                    showCloseButton: false,
                    timer: 3000,
                });
            }
            this.dialog = false
        },
        //解決する前に，ベストアンサーがあるか判定[ok]
        hasBestAnswer(answer_list) {
            let best_answer_decision = false
            for (let item of answer_list) {
                if ( item.answer_best == true) {
                    console.log('ベストアンサーあり')
                    best_answer_decision = true
                    this.best_answer_has = true

                }
            }
            return best_answer_decision
        },
        log() {   
        }
    },
}
</script>