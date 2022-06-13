<template>
  <v-app>
    <Header />
    <v-main>
      <NavHelpBar />
      <v-container fluid>
        <v-card v-for="item in unresolved_question" :key="item.id">
          <v-card-text>
            <router-link :to="{ name: 'question-detail', params: { id: item.id } }">
              {{ item.question_title }} {{ item.question_post_time }}
            </router-link>
            <!-- <router-link :to="{ name: 'content-url', params: {id: Number(id) + 1 } }">リンク名</router-link> -->

          </v-card-text>
        </v-card>
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
import Header from "../components/Header.vue";
import NavHelpBar from "../components/NavigationHelpBar.vue"
import axios from "axios";
//import changeTimestamp from "../node/changeTimestamp";

export default {
  components: {
    Header, NavHelpBar,
  },
  data() {
    return {
      tab: null,
      unresolved_question: {},
      resolved_question: {},
      my_question: {},
      logtest: [{ id: 1, title: 'title1', content: '2022-05-25', }, { id: 2, title: 'title2', content: '2022-05-24' }, { id: 3, title: 'title3', content: '2022-05-13' }],
      items: [
        //{ tab: '未解決', testcontent: [{ id: 1, title: 'title1', content: '2022-05-25', }, { id: 2, title: 'title2', content: '2022-05-24' }, { id: 3, title: 'title3', content: '2022-05-13' }], },
        { tab: '未解決', content: this.logtest, },
        { tab: '解決済み', content: [{ id: 4, question_title: 'title1', content: 'a' }, { id: 5, question_title: 'title2', content: 'b' }, { id: 6, question_title: 'title3', content: 'c' }], },
        { tab: '評価の高い質問', content: [{ id: 7, question_title: 'title1', content: 'あ' }, { id: 8, question_title: 'title2', content: 'い' }, { id: 9, question_title: 'title3', content: 'う' }], },
        // { tab: '自分の質問', testcontent: [{ id: 10, title: 'title1', content: '1' }, { id: 11, title: 'title2', content: '2' }], },
      ],
    }
  },
  mounted() {
    this.getUnresolvedQuestion()
  },
  methods: {
    getUnresolvedQuestion() {
      axios
        .get(process.env.VUE_APP_API_URL + "/app/get-question/unresolved/")
        .then((res) => {
          console.log(res.data);
          //let timestamp = changeTimestamp(res.data)
          //console.log(timestamp)
          this.unresolved_question = res.data
        })
        .catch((e) => {
          console.log(e);
        });
    },
    getResolvedQuestion() {
      axios
        .get(process.env.VUE_APP_API_URL + "/app/get-question/resolved/")
        .then((res) => {
          console.log(res.data);
          this.resolved_question = res.data
        })

        .catch((e) => {
          console.log(e);
        });
    },
    //未完成
    getMyQuestion() {
      axios
        .get(process.env.VUE_APP_API_URL + "/app/get-question/")
        .then((res) => {
          console.log(res.data);
          //res.dateを保持する
        })
        .catch((e) => {
          console.log(e);
        });
    },
  }
}
</script>