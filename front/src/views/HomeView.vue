<template>
  <v-app>
    <Header />
    <div class="row justify-content-center">
      <!--質問タブ-->
      <v-card class="mx-auto" max-height="344">
        <v-col class="mb-10">
          <router-link to='/question'>
            <v-btn color="primary">質問する</v-btn>
          </router-link>
          <v-tabs v-model="tab">
            <v-tab v-for="item in items" :key="item.tab">
              {{ item.tab }}
            </v-tab>
          </v-tabs>
          <!--質問-->
          <v-tabs-items v-model="tab">
            <v-tabs-items v-model="tab">
              <v-tab-item v-for="item in items" :key="item.tab">
                <v-card v-for="question in item.testcontent" :key="question.content">
                  <v-card-text>{{ question.title }} {{ question.content }}</v-card-text>
                </v-card>
              </v-tab-item>
            </v-tabs-items>
          </v-tabs-items>
        </v-col>
      </v-card>
    </div>
  </v-app>
</template>

<script>
import Header from "../components/Header.vue";
export default {
  components: {
    Header,
  },
  data() {
    return {
      tab: null,
      //contentをそれぞれ取得して、保存するようにする(mount())
      //title timestamp answer数
      items: [
        // { tab: '未解決', content: 'Please Help me' },
        { tab: '未解決', testcontent: [{ id: 1, title: 'title1', content: '2022-05-25', }, { id: 2, title: 'title2', content: '2022-05-24' }, { id: 3, title: 'title3', content: '2022-05-13' }], },
        { tab: '解決済み', testcontent: [{ id: 4, title: 'title1', content: 'a' }, { id: 5, title: 'title2', content: 'b' }, { id: 6, title: 'title3', content: 'c' }], },
        { tab: '評価の高い質問', testcontent: [{ id: 7, title: 'title1', content: 'あ' }, { id: 8, title: 'title2', content: 'い' }, { id: 9, title: 'title3', content: 'う' }], },
        { tab: '自分の質問', testcontent: [{ id: 10, title: 'title1', content: '1' }, { id: 11, title: 'title2', content: '2' }], },
      ],
    }
  },
}
</script>