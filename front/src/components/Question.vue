<template>
  <v-card>
    <v-tabs v-model="tab">
      <v-tab v-for="item in items" :key="item.tab">
        {{ item.tab }}
      </v-tab>
    </v-tabs>

    <v-tabs-items v-model="tab">
      <v-tab-item v-for="item in items" :key="item.tab">
        <v-card flat>
          <!--v-forで質問を表示する クリックしたら閲覧できるようにする-->
          <v-card-text>{{ item.content }}</v-card-text>
        </v-card>
      </v-tab-item>
    </v-tabs-items>
  </v-card>
</template>

<script>
export default {
  data() {
    return {
      tab: null,
      currentItem: "未解決",
      items: [
        { tab: '未解決', content: 'Please Help me' },
        { tab: '解決済み', content: 'Finish' },
        { tab: '評価の高い質問', content: 'Best Question' },
        { tab: '自分の質問', content: '質問はありません' },
      ],
    }
  },
}
</script>