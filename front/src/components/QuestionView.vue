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
                    <v-card-title>回答 {{ item.id }}</v-card-title>
                    <v-card-text>{{ item.answer_content }}</v-card-text>
                    <v-card-text>{{ item.answer_source_code }}</v-card-text>
                    <v-card-actions>
                        <v-btn color="orange" text>
                            高評価
                        </v-btn>
                    </v-card-actions>
                </v-card>
                <v-card class="mt-10">
                    <v-card-title>
                        回答フォーム
                    </v-card-title>
                    <v-form>
                        <v-textarea background-color="grey lighten-2" label="質問内容"></v-textarea>
                        <v-textarea background-color="blue" label="ソースコード"></v-textarea>
                    </v-form>
                </v-card>
            </v-container>
        </v-main>
    </v-app>
</template>

<script>
//idを元に質問とその質問に対する回答を取得．さらに回答フォームを作る
import Header from "../components/Header.vue";
import NavHelpBar from "../components/NavigationHelpBar.vue"
import axios from "axios";

export default {
    components: { Header, NavHelpBar },
    data() {
        return {
            one_quesiton: {},
            any_answer: {},
            id: this.$route.params.id,
            question_id: 0,
        };
    },
    mounted() {
        this.getOneQuestion()
        this.getAnyAnswer()
    },
    methods: {
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
        log() {
            console.log(this.id)
        }
    },
}
</script>