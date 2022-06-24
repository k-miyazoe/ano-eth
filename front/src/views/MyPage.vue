<template>
    <v-app>
        <Header />
        <v-main>
            <NavHelpBar />
            <v-container grid-list-md>
            </v-container>
        </v-main>
    </v-app>
</template>

<script>
import axios from "axios";
import Swal from "sweetalert2";
import router from "../router";
import Header from "../components/Header.vue";
import NavHelpBar from "../components/NavigationHelpBar.vue"

export default {
    components: {
        Header, NavHelpBar,
    },
    data: () => ({
        //urlパラメータ取得
        uid: this.$route.params.id,
        valid: true,
        loading: false,
        axios: {},
        user_id: null,
    }),
    mounted() {
        this.checkToken();
    },
    methods: {
        //useridを取得してuser情報をひょうじする　
        checkToken() {
            this.$session.start();
            if (this.$session.has("token")) {

            }
        },
    },

}
</script>