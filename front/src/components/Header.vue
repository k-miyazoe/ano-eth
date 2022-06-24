<template>
  <div>
    <v-app-bar color="#00B0FF" dense dark elevation="10">
      <v-toolbar-title>
        プログラミング概論・質問掲示板
      </v-toolbar-title>
      <v-spacer />
      <v-btn>
        <router-link to='/signup'>
          サインアップ
        </router-link>
      </v-btn>
      <v-btn>
        <router-link to='/signin'>
          サインイン
        </router-link>
      </v-btn>
      <v-btn>
        <router-link to='/mypage'>
          マイページ
        </router-link>
      </v-btn>
    </v-app-bar>
    <div style="padding: 15px;"></div>
  </div>
</template>

<script>
import axios from "axios";
export default {
  components: {
  },
  data: () => ({
    uid: 1,
  }),
  mounted() {
    this.setURLParameter();
  },
  methods: {
    setURLParameter() {
      this.$session.start();
      if (this.$session.has("token")) {
        console.log('Header.vue set uid', this.$session.get('user_id'))
        this.uid = this.$session.get('user_id')
      }
    },
  },

}

</script>
