<template>
    <v-app>
        <v-navigation-drawer
                v-model="drawer"
                app
        >
            <v-list dense>

                <router-link to="/" class="v-list-item v-list-item--link theme--light">
                    <v-list-item-action>
                        <v-icon>mdi-home</v-icon>
                    </v-list-item-action>
                    <v-list-item-content>
                        <v-list-item-title>Главная</v-list-item-title>
                    </v-list-item-content>
                </router-link>

                <!--<router-link to="/adverts" class="v-list-item v-list-item&#45;&#45;link theme&#45;&#45;light">-->
                    <!--<v-list-item-action>-->
                        <!--<v-icon>mdi-card-text-outline</v-icon>-->
                    <!--</v-list-item-action>-->
                    <!--<v-list-item-content>-->
                        <!--<v-list-item-title>Объявления</v-list-item-title>-->
                    <!--</v-list-item-content>-->
                <!--</router-link>-->

                <router-link to="/apply" class="v-list-item v-list-item--link theme--light">
                    <v-list-item-action>
                        <v-icon>mdi-card-plus-outline</v-icon>
                    </v-list-item-action>
                    <v-list-item-content>
                        <v-list-item-title>Подать объявление</v-list-item-title>
                    </v-list-item-content>
                </router-link>

                <router-link to="/login" class="v-list-item v-list-item--link theme--light" v-if="!auth">
                    <v-list-item-action>
                        <v-icon>mdi-login-variant</v-icon>
                    </v-list-item-action>
                    <v-list-item-content>
                        <v-list-item-title>Вход</v-list-item-title>
                    </v-list-item-content>
                </router-link>

                <router-link to="/registration" class="v-list-item v-list-item--link theme--light" v-if="!auth">
                    <v-list-item-action>
                        <v-icon>mdi-account-plus-outline</v-icon>
                    </v-list-item-action>
                    <v-list-item-content>
                        <v-list-item-title>Регистрация</v-list-item-title>
                    </v-list-item-content>
                </router-link>

                <router-link to="/my-adverts" class="v-list-item v-list-item--link theme--light" v-if="auth">
                    <v-list-item-action>
                        <v-icon>mdi-cards-variant</v-icon>
                    </v-list-item-action>
                    <v-list-item-content>
                        <v-list-item-title>Мои объявления</v-list-item-title>
                    </v-list-item-content>
                </router-link>

                <v-list-item link v-if="auth" @click="logout()">
                    <v-list-item-action>
                        <v-icon>mdi-logout</v-icon>
                    </v-list-item-action>
                    <v-list-item-content>
                        <v-list-item-title>Выход</v-list-item-title>
                    </v-list-item-content>
                </v-list-item>

            </v-list>
        </v-navigation-drawer>

        <v-app-bar
                app
                color="indigo"
                dark
        >
            <v-app-bar-nav-icon @click.stop="drawer = !drawer"/>
            <v-toolbar-title>Applebar</v-toolbar-title>
        </v-app-bar>

        <v-content>
            <router-view :auth="auth" v-on:check_auth="onCheckAuth"></router-view>
        </v-content>

        <v-footer
                color="indigo"
                app
        >
            <span class="white--text">&copy; 2020</span>
        </v-footer>
    </v-app>
</template>

<script>
    import $ from 'jquery'

    export default {
        name: 'app',
        data: () => ({
            drawer: false,
            auth: sessionStorage.getItem("auth_token") ? true : false
        }),
        computed: {
        },
        created: function () {
        },
        methods: {
            onCheckAuth(boolean) {
                this.auth = boolean
            },
            logout() {
                sessionStorage.removeItem("auth_token")
                this.$router.push('/')
                this.auth = false
                try {
                    delete $.ajaxSettings.headers["Authorization"]
                } catch (e) {
                    this.auth = false
                }
            }
        },
        props: {
            source: String,
        }
    }
</script>

<style>
    .login {
        float: right;
    }
</style>