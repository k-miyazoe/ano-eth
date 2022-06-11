<template>
    <v-app>
        <Header />
        <div class="row justify-content-center">
            <v-card class="mx-auto" max-height="344">
                <v-col class="mb-10">
                    <v-card>
                        <v-card-text>{{ one_quesiton.question_title }}</v-card-text>
                        <v-card-text>{{ one_quesiton.question_content }}</v-card-text>
                    </v-card>
                </v-col>
            </v-card>
        </div>

    </v-app>
</template>

<script>
//idを元に質問とその質問に対する回答を取得．さらに回答フォームを作る
import Header from "../components/Header.vue";
import axios from "axios";

export default {
    components: { Header },
    data() {
        return {
            one_quesiton: {},
            id: this.$route.params.id,
        };
    },
    mounted() {
        this.getOneQuestion()
        //this.log()
    },
    methods: {
        getOneQuestion() {
            axios
                .get(process.env.VUE_APP_API_URL + "/app/get-question/" + this.id)
                .then((res) => {
                    console.log(res.data);
                    this.one_quesiton = res.data
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