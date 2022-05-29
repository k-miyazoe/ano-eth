<template>
  <v-app>
    <Header />
    <v-container>
      <v-card class="mt-12">
        <v-card-title>
          <span class="headline">質問フォーム</span>
        </v-card-title>

        <v-layout row fill-height justify-center align-center v-if="loading">
          <v-progress-circular :size="50" color="primary" indeterminate />
        </v-layout>

        <!-- 質門投稿フォーム -->
        <v-form v-else ref="form" v-model="valid" lazy-validation>
          <!--title-->
          <v-textarea background-color="grey" color="black" label="質問タイトル" clearable clear-icon="mdi-close-circle"
            rows="1" outlined>
          </v-textarea>
          <!--content-->
          <v-textarea background-color="grey lighten-2" color="orange orange-darken-4" label="質問内容" clearable
            clear-icon="mdi-close-circle" auto-grow outlined>
          </v-textarea>
          <!--sorce code-->
          <v-textarea background-color="blue" color="cyan" label="ソースコード" clearable clear-icon="mdi-close-circle"
            auto-grow outlined>
          </v-textarea>
          <v-btn variant="outline-primary" :disabled="!valid">質問する</v-btn>
        </v-form>
      </v-card>
    </v-container>
  </v-app>
</template>
<script>
import { VueLoading } from 'vue-loading-template'
import Header from "../components/Header.vue";

export default {
  components: {
    VueLoading,
    Header
  },
  data() {
    return {
      title: '',
      contents: '',
      already_perfect: false,
      miner: '0x4c4941fb0a0f300b615a9d5e9fb215d2db35c7ec',
      host: 'https://eagle4.fu.is.saga-u.ac.jp/geth-docker/',
      loading: false,
      valid: true,
    };
  },
  methods: {
  }
}
</script>