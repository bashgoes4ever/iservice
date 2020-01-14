<template>
    <v-container
            class="fill-height"
            fluid
    >
        <v-row
                align="center"
                justify="center"
        >
            <v-col
                    cols="12"
                    sm="8"
                    md="4"
            >
                <v-card class="elevation-12">
                    <v-toolbar
                            color="indigo"
                            dark
                            flat
                    >
                        <v-toolbar-title>Форма входа</v-toolbar-title>
                        <v-spacer/>
                    </v-toolbar>
                    <v-card-text>
                        <v-form>
                            <v-text-field
                                    label="Ваш номер телефона"
                                    name="phone"
                                    prepend-icon="mdi-cellphone-android"
                                    type="tel"
                                    v-model="username"
                            />

                            <v-text-field
                                    id="password"
                                    label="Ваш пароль"
                                    name="password"
                                    prepend-icon="mdi-lock"
                                    type="password"
                                    v-model="password"
                            />
                            <p v-if="hasError" class="red--text">{{error_text}}</p>
                        </v-form>
                    </v-card-text>
                    <v-card-actions>
                        <v-spacer/>
                        <v-btn color="indigo" class="white--text" @click="login()">Войти</v-btn>
                    </v-card-actions>
                </v-card>
            </v-col>
        </v-row>
    </v-container>
</template>

<script>
    import $ from 'jquery'

    export default {
        name: "Login",
        data: () => ({
            error: {},
            hasError: false,
            username: '',
            password: '',
        }),
        created: function () {
        },
        methods: {
            login() {
                var phone = this.username.replace(/[^0-9]/gim,'')
                if (phone[0] == '8') {
                    var temp = phone.split('')
                    temp[0] = '7'
                    phone = temp.join('')
                }
                $.ajax({
                    url: 'http://178.21.8.217/auth/token/login/',
                    data: {
                        'username': phone,
                        'password': this.password
                    },
                    type: 'POST',
                    success: (response) => {
                        sessionStorage.setItem("auth_token", response.auth_token)
                        this.$emit('check_auth', true)
                        this.$router.push('/')
                    },
                    error: (err) => {
                        if (err.status === 400) {
                            this.hasError = true
                            this.error_text = "Неправильные логин или пароль"
                        }
                    }
                })
            }
        },
        props: ['auth']
    }
</script>

<style scoped>

</style>