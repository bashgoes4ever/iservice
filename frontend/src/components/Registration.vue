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
                        <v-toolbar-title>Форма регистрации</v-toolbar-title>
                        <v-spacer/>
                    </v-toolbar>
                    <v-card-text>
                        <v-form>
                            <v-text-field
                                    label="Ваш номер телефона"
                                    name="phone"
                                    prepend-icon="mdi-cellphone-android"
                                    type="tel"
                            />
                            <p>Мы вышлем на введенный Вами номер смс с паролем, после чего вы сможете зайти на сайт и подать объявление.</p>
                            <p v-if="hasError" class="red--text">{{error.error}}</p>

                        </v-form>
                    </v-card-text>
                    <v-card-actions>
                        <v-spacer/>
                        <v-btn color="indigo" class="white--text" @click="register()">Регистрация
                        </v-btn>
                    </v-card-actions>
                </v-card>
            </v-col>
        </v-row>
    </v-container>
</template>

<script>
    import $ from 'jquery'

    export default {
        name: "Registration",
        data: () => ({
            error: {},
            hasError: false
        }),
        created: function () {
        },
        methods: {
            register() {
                $.ajax({
                    url: 'http://178.21.8.217/api/v1/register/',
                    data: {'phone': $('input[name="phone"]').val()},
                    type: 'POST',
                    success: (data) => {
                        if (data['code'] == 0) {
                            this.$router.push('/login')
                        } else {
                           this.error = data
                            this.hasError = true
                        }
                    }
                })
            }
        }
    }
</script>

<style scoped>

</style>