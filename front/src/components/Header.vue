<template>
  <div>
    <v-app-bar color="#00B0FF" dense dark elevation="10">
      <v-toolbar-title>
        <router-link to='/'>
          ANO-ETH
        </router-link>
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
      <v-btn icon>
        <router-link to='/'>
          <v-icon>mdi-trophy-variant-outline</v-icon>
        </router-link>
      </v-btn>
      <v-btn icon>
        <router-link to='/question'>
          <v-icon>mdi-lightbulb-question-outline</v-icon>
        </router-link>
      </v-btn>
    </v-app-bar>
    <div style="padding: 15px;"></div>
  </div>
</template>

<script>
</script>
