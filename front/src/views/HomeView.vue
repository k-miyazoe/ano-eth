<template>
  <v-app>
    <v-main class="grey lighten-2">
        <v-row class="col-md-6 offset-md-3">
          <v-col class="mt-4" align="start">
            <v-toolbar color="#78909C" dark flat class="rounded-t-xl">
              <template v-slot:extension>
                <v-tabs v-model="tab" align-with-title @change="check_tab()">
                  <v-tabs-slider color="yellow"></v-tabs-slider>
                  <v-tab v-for="item in items" :key="item">
                    <v-badge
                      v-if="question_list[item]['is_new']"
                      color="red"
                      :content="question_list[item]['is_new']"
                    >
                      {{ item }}
                    </v-badge>
                    <div v-else>
                      {{ item }}
                    </div>
                  </v-tab>
                </v-tabs>
              </template>
            </v-toolbar>
            <v-tabs-items v-model="tab" @change="check_tab()">
              <v-tab-item v-for="item in items" :key="item">
                <v-expansion-panels
                  v-for="question in question_list[item]['value']"
                  :key="question"
                  focusable
                >
                  <v-expansion-panel>
                    <v-expansion-panel-header>
                      {{ question }}
                    </v-expansion-panel-header>
                    <v-expansion-panel-content>
                      <p></p>
                      {{ question }}
                    </v-expansion-panel-content>
                  </v-expansion-panel>
                </v-expansion-panels>
              </v-tab-item>
            </v-tabs-items>
          </v-col>
        </v-row>
    </v-main>
  </v-app>
</template>
<script>
import router from '../router';
export default ({
  data: () => ({
    items: ["未解決", "解決済み", "自分の質問"],
    tab: null,
    //ここはDBから持ってきたほうがいい
    question_list: {
      未解決: { is_new: 0, value: ["0_hello", "0_hoge"] },
      解決済み: { is_new: 2, value: ["1_hello", "1_hoge"] },
      自分の質問: { is_new: 4, value: ["2_hello", "2_hoge"] },
    },
  }),
  mounted(){
    this.checkLoggedIn();
  },
  methods: {
    // 確認したタブのバッジを削除する
    check_tab() {
      this.question_list[this.items[this.tab]]["is_new"] = 0;
      // TODO : DBに見たことを記すデータを反映させる
    },
    checkLoggedIn(){
      this.$session.start()
      if(!this.$session.has('token')){
        router.push('/signin')
      }
    },
  }
  
})
</script>

