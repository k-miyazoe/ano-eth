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
                <!--解決済み-->
                <div v-if="one_quesiton.question_status">
                    <v-card class="mx-auto" max-height="344">
                        <v-col class="mb-10">
                            <!--質問タイトル-->
                            <v-card-title>質問 {{ one_quesiton.question_title }} 解決済み!
                                <v-card-subtitle>質問者:{{ one_quesiton.question_user_name }}</v-card-subtitle>
                            </v-card-title>
                            <!--質問内容-->
                            <v-card>
                                <v-card-subtitle>内容</v-card-subtitle>
                                <v-card-text>{{ one_quesiton.question_content }}</v-card-text>
                            </v-card>
                            <!--ソースコード-->
                            <v-card>
                                <v-card-subtitle>ソースコード</v-card-subtitle>
                                <v-card-text>{{ one_quesiton.question_source_code }}</v-card-text>
                            </v-card>

                            <v-card-actions>
                                <!--高評価-->
                                <v-btn color="orange" text @click="highlyRatedQuestion">
                                    <v-icon>mdi-thumb-up</v-icon>
                                    {{ one_quesiton.question_value }}
                                </v-btn>
                                <!--解決を解除-->
                                <v-btn color="green" text @click="releaseResolvedQuestion">
                                    解決取り消し
                                </v-btn>
                            </v-card-actions>
                        </v-col>
                    </v-card>
                </div>
                <!--未解決-->
                <div v-else>
                    <v-card class="mx-auto" max-height="344">
                        <v-col class="mb-10">
                            <!--質問タイトル-->
                            <v-card-title>質問 {{ one_quesiton.question_title }}
                                <v-card-subtitle>質問者:{{ one_quesiton.question_user_name }}</v-card-subtitle>
                            </v-card-title>
                            <!--質問内容-->
                            <v-card>
                                <v-card-subtitle>内容</v-card-subtitle>
                                <v-card-text>{{ one_quesiton.question_content }}</v-card-text>
                            </v-card>
                            <!--ソースコード-->
                            <v-card>
                                <v-card-subtitle>ソースコード</v-card-subtitle>
                                <v-card-text>{{ one_quesiton.question_source_code }}</v-card-text>
                            </v-card>

                            <v-card-actions>
                                <!--高評価-->
                                <v-btn color="orange" text @click="highlyRatedQuestion">
                                    <v-icon>mdi-thumb-up</v-icon>
                                    {{ one_quesiton.question_value }}
                                </v-btn>
                                <!--解決-->
                                <v-btn color="green" text @click="resolvedQuestion">
                                    解決
                                </v-btn>
                            </v-card-actions>
                        </v-col>
                    </v-card>
                </div>
                <v-divider></v-divider>

                <!--回答一覧-->
                <v-card v-for="(item, index) in any_answer" :key="index">
                    <!--ベストアンサーの回答-->
                    <div v-if="item.answer_best">
                        <v-card-title>回答 {{ index + 1 }} ベストアンサー</v-card-title>
                        <v-card-subtitle>回答者:{{ item.answer_user_name }}</v-card-subtitle>
                        <v-card-text>{{ item.answer_content }}</v-card-text>
                        <v-card-text>{{ item.answer_source_code }}</v-card-text>
                        <v-card-actions>
                            <!--いいねボタン-->
                            <v-btn color="orange" text @click="highlyRatedAnswer(index)">
                                <v-icon>mdi-thumb-up</v-icon>
                                {{ item.answer_value }}
                            </v-btn>
                            <!--ベストアンサ解除ー-->
                            <v-btn color="red" text @click="releaseBestAnswer(item)">
                                解除
                            </v-btn>
                        </v-card-actions>
                    </div>
                    <!--ベストアンサーではない回答-->
                    <div v-else>
                        <v-card-title>回答 {{ index + 1 }}</v-card-title>
                        <v-card-subtitle>回答者:{{ item.answer_user_name }}</v-card-subtitle>
                        <v-card-text>{{ item.answer_content }}</v-card-text>
                        <v-card-text>{{ item.answer_source_code }}</v-card-text>
                        <v-card-actions>
                            <!--いいねボタン-->
                            <v-btn color="orange" text @click="highlyRatedAnswer(index)">
                                <v-icon>mdi-thumb-up</v-icon>
                                {{ item.answer_value }}
                            </v-btn>
                            <!--ベストアンサー-->
                            <v-btn color="red" text @click="bestAnswer(item)">
                                ベストアンサー
                            </v-btn>
                        </v-card-actions>
                    </div>
                </v-card>
                <!--回答フォーム-->
                <v-card class="mt-10">
                    <v-card-title>
                        回答フォーム
                    </v-card-title>
                    <v-form ref="form" v-model="valid" lazy-validation>
                        <v-textarea v-model="credentials.answer_content" label="解決策・提案*" :rules="rules.answer_content"
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
        NavHelpBar,
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
            ether_user_name: null,
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
                    console.log('getEtherId', data["user_name"])
                    this.ether_user_name = data["user_name"]
                })
                .catch((e) => {
                    console.log(e);
                });
        },
        //解決する前に，ベストアンサーがあるか判定[ok] 引数obj型
        hasBestAnswer(answer_list) {
            let best_answer_decision = false
            for (let item of answer_list) {
                if (item.answer_best == true) {
                    console.log('ベストアンサーあり')
                    best_answer_decision = true
                    this.best_answer_has = true
                }
            }
            return best_answer_decision
        },

        //イベント処理

        //回答送信 ok
        postAnswer() {
            this.loading = true
            this.credentials["ether_id"] = this.etherId
            this.credentials["question_id"] = this.question_id
            //回答者名が反映されてない aなら実名，それ以外なら匿名 判定するプログラムが必要
            this.credentials["answer_user_name"] = this.ether_user_name
            this.axios
                .post(process.env.VUE_APP_API_URL + "/app/create-answer/", this.credentials)
                .then((res) => {
                    console.log(res);
                    this.loading = false
                    this.credentials = {}
                    //point追加
                    this.putSendPoint()
                    this.getAnyAnswer()
                    //質問の回答数追加
                    this.numberOfResponses()
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
        //質問の回答数をカウントアップする
        numberOfResponses() {
            let obj = {
                ether_id: this.one_quesiton.ether_id,
                question_number_of_responses: this.one_quesiton.question_number_of_responses + 1,
            }
            this.axios
                .put(process.env.VUE_APP_API_URL + "/app/update-question/" + this.question_id + "/", obj)
                .then((res) => {
                    console.log("質問の回答数増加", res);
                })
                .catch((e) => {
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
        //質問のいいね機能 ok
        highlyRatedQuestion() {
            let question_like_obj = {
                user: this.userId,//現在のuserid
                question_id: this.one_quesiton.id,
            }
            console.log('obj check', question_like_obj)
            this.axios
                .post(process.env.VUE_APP_API_URL + "/app/question-like/", question_like_obj)
                .then((res) => {
                    console.log(res.data);
                    console.log('評価が変更されました')
                    this.getOneQuestion()
                })
                .catch((e) => {
                    console.log(e);
                });
        },
        //質問解決
        resolvedQuestion() {
            //質問者かどうか
            if (this.etherId == this.one_quesiton.ether_id) {
                //回答が存在する場合
                //ここのifのじょうけんがうまくいってない
                if (this.any_answer.length != 0) {
                    //ベストアンサーが存在しているなら
                    if (this.best_answer_has) {
                        //解決処理
                        let resolve_obj = {
                            ether_id: this.one_quesiton.ether_id,
                            question_status: true
                        }
                        this.axios
                            .put(process.env.VUE_APP_API_URL + "/app/update-question/" + this.question_id + "/", resolve_obj)
                            .then((res) => {
                                console.log(res);
                                Swal.fire(
                                    '質問が解決されました!',
                                    'success',
                                )
                                this.getOneQuestion()
                            })
                            .catch((e) => {
                                console.log(e);
                            });
                    }
                    //ベストアンサーが存在してない場合
                    else {
                        Swal.fire({
                            icon: "warning",
                            title: "Error",
                            text: "ベストアンサーが存在しません．ベストアンサーを選択してください!",
                            showConfirmButton: false,
                            showCloseButton: false,
                            timer: 3000,
                        });
                    }
                }
                //回答がない場合
                else {
                    Swal.fire({
                        icon: "warning",
                        title: "Error",
                        text: "回答が存在しません.自己解決した場合、自身で回答を作成してください",
                        showConfirmButton: false,
                        showCloseButton: false,
                        timer: 3000,
                    });
                }
            }
            //質問者以外
            else {
                Swal.fire({
                    icon: "warning",
                    title: "Error",
                    text: "質問者のみ有効です！",
                    showConfirmButton: false,
                    showCloseButton: false,
                    timer: 3000,
                });
            }
        },
        //質問解決解除
        releaseResolvedQuestion() {
            if (this.etherId == this.one_quesiton.ether_id) {
                let release_resolve_obj = {
                    ether_id: this.one_quesiton.ether_id,
                    question_status: false
                }
                this.axios
                    .put(process.env.VUE_APP_API_URL + "/app/update-question/" + this.question_id + "/", release_resolve_obj)
                    .then((res) => {
                        Swal.fire(
                            '解決を取り消しました!',
                            'success',
                        )
                        this.getOneQuestion()
                    })
                    .catch((e) => {
                        console.log(e);
                    });
            }
            else {
                Swal.fire({
                    icon: "warning",
                    title: "Error",
                    text: "質問者のみ有効です！",
                    showConfirmButton: false,
                    showCloseButton: false,
                    timer: 3000,
                });
            }
        },
        //回答のいいね機能 ok
        highlyRatedAnswer(answer_index) {
            //回答の評価値を1上げる 回答した人のetheridが必要
            let answer_like_obj = {
                user: this.userId,
                answer_id: this.any_answer[answer_index].id
            }
            this.axios
                .post(process.env.VUE_APP_API_URL + "/app/answer-like/", answer_like_obj)
                .then((res) => {
                    console.log(res);
                    console.log('評価が変更されました')
                    this.getAnyAnswer()
                })
                .catch((e) => {
                    console.log(e);
                });
        },
        //bestanswer処理 ok
        bestAnswer(answer) {
            //bestアンサーがすでに存在している場合
            if (this.best_answer_has) {
                Swal.fire({
                    icon: "warning",
                    title: "Error",
                    text: "すでにベストアンサーは存在しています！",
                    showConfirmButton: false,
                    showCloseButton: false,
                    timer: 3000,
                });
            }
            //bestanswerがない場合
            else {
                //質問者のみベストアンサー決定可能
                if (this.etherId == this.one_quesiton.ether_id) {
                    let answer_update_obj = {
                        ether_id: answer.ether_id,
                        question_id: this.question_id,
                        answer_best: true
                    }
                    this.axios
                        .put(process.env.VUE_APP_API_URL + "/app/update-answer/" + answer.id + "/", answer_update_obj)
                        .then((res) => {
                            this.best_answer_has = true
                            console.log(res);
                            Swal.fire(
                                'ベストアンサーを決定しました!',
                                'success',
                            )
                            //ページの更新
                            this.getAnyAnswer()
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
            }
        },
        //bestanswer解除処理
        releaseBestAnswer(answer) {
            if (this.etherId == this.one_quesiton.ether_id) {
                let answer_release_obj = {
                    ether_id: answer.ether_id,
                    //ether_id: this.any_answer[answer_list_index].ether_id,
                    question_id: this.question_id,
                    answer_best: false
                }
                this.axios
                    .put(process.env.VUE_APP_API_URL + "/app/update-answer/" + answer.id + "/", answer_release_obj)
                    .then((res) => {
                        this.best_answer_has = false
                        console.log(res);
                        Swal.fire(
                            'ベストアンサーを解除しました!',
                            'success',
                        )
                        //ページの更新
                        this.getAnyAnswer()
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
                    text: "質問者のみベストアンサーを解除できます",
                    showConfirmButton: false,
                    showCloseButton: false,
                    timer: 3000,
                });
            }
        },
        //メール通知機能 obj作ってpostする
        mailSend() {
            let mail_obj = {
                subject: answer.ether_id,
                message: this.question_id,
                receipt_email: null,
            }
            this.axios
                .post(process.env.VUE_APP_API_URL + "/app/create-answer/", mail_obj)
                .then((res) => {
                })
                .catch((e) => {
                });
        },
        log() {
            console.log('any_answer', this.any_answer.length)
            //console.log('length')
        }
    },
}
</script>