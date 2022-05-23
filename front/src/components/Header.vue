<template>
  <div>
    <v-app-bar color="#00B0FF" dense dark elevation="10">
      <v-spacer />
      <v-toolbar-title>VCEA</v-toolbar-title>
      <v-spacer />
      <v-row>
        <v-col cols="12" sm="6">
          <v-textarea label="検索" auto-grow outlined rows="1" row-height="15"></v-textarea>
        </v-col>
      </v-row>

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
  </div>
</template>

<script>
</script>
