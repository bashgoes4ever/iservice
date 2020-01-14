<template>
    <v-container>
        <div class="block1">
            <h1>Мои объявления</h1>
            <div class="block2__flex">

                <div class="block2__item" v-for="(advert, i) in adverts" :key="i">
                    <div class="block2__img"
                         v-if="advert.images.length > 0"
                         :style="`background-image: url(http://178.21.8.217/${getMainImage(advert.images)})`">

                        <v-chip
                                class="ma-2"
                                color="green"
                                text-color="white"
                                v-if="advert.moderated"
                        >
                            <v-avatar left>
                                <v-icon>mdi-check</v-icon>
                            </v-avatar>
                            Прошло модерацию
                        </v-chip>

                        <v-chip
                                class="ma-2"
                                color="orange"
                                text-color="white"
                                v-else
                        >
                            <v-avatar left>
                                <v-icon>mdi-timer-sand</v-icon>
                            </v-avatar>
                            На модерации
                        </v-chip>

                    </div>
                    <div class="block2__img"
                         v-else
                         style="background: #f0f0f0;">

                        <v-chip
                                class="ma-2"
                                color="green"
                                text-color="white"
                                v-if="advert.moderated"
                        >
                            <v-avatar left>
                                <v-icon>mdi-check</v-icon>
                            </v-avatar>
                            Прошло модерацию
                        </v-chip>

                        <v-chip
                                class="ma-2"
                                color="orange"
                                text-color="white"
                                v-else
                        >
                            <v-avatar left>
                                <v-icon>mdi-timer-sand</v-icon>
                            </v-avatar>
                            На модерации
                        </v-chip>

                    </div>
                    <div class="block2__text">
                        <router-link class="h3" :to="`/adverts/${advert.id}`">{{advert.title}} - <span>{{advert.price}} руб</span>
                        </router-link>
                        <div class="category">Категория: {{advert.category.name}} {{advert.product.name}}</div>
                        <div class="date">{{formatDate(advert.created)}}</div>
                        <v-btn color="red" fab small dark class="delete" @click.stop="openDialog(advert.id, i)">
                            <v-icon>mdi-delete</v-icon>
                        </v-btn>
                        <v-btn color="primary" fab small dark class="edit" :to="`/my-adverts/${advert.id}`">
                            <v-icon>mdi-pencil</v-icon>
                        </v-btn>
                    </div>
                </div>

            </div>
        </div>
        <v-dialog
                v-model="dialog"
                max-width="310"
        >
            <v-card>
                <v-card-title class="headline">Удалить объявление?</v-card-title>

                <v-card-actions>
                    <v-spacer></v-spacer>

                    <v-btn
                            color="indigo darken-1"
                            text
                            @click="dialog = false"
                    >
                        Нет
                    </v-btn>

                    <v-btn
                            color="indigo darken-1"
                            text
                            @click="deleteAdvert(current_id, current_index)"
                    >
                        Да
                    </v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>
    </v-container>
</template>

<script>
    import $ from 'jquery'
    import moment from 'moment'

    export default {
        name: "MyAdverts",
        data: () => ({
            user_id: 0,
            adverts: [],
            dialog: false,
            current_id: 0,
            current_index: 0
        }),
        created: function () {
            if (sessionStorage.getItem("auth_token")) {
                $.ajaxSetup({
                    headers: {'Authorization': "Token " + sessionStorage.getItem('auth_token')},
                });
            }
            this.getUser()
        },
        methods: {
            getUser() {
                $.ajax({
                    url: 'http://178.21.8.217/auth/users/me/',
                    type: 'GET',
                    success: (data) => {
                        this.user_id = data.id
                        this.getAdverts(this.user_id)
                    }
                })
            },
            getAdverts(user_id) {
                $.ajax({
                    url: `http://178.21.8.217/api/v1/user_adverts/${user_id}`,
                    type: 'GET',
                    success: (data) => {
                        this.adverts = data.data
                    }
                })
            },
            getMainImage(images) {
                let result = images.find(obj => {
                    return obj.is_main === true
                })
                return result.image_thumb
            },
            formatDate(date) {
                return moment(date).format('DD.MM.YYYY')
            },
            deleteAdvert(id, index) {
                $.ajax({
                    url: `http://178.21.8.217/api/v1/delete_advert/${id}`,
                    type: 'DELETE',
                    success: () => {
                        this.adverts.splice(index, 1)
                        this.dialog = false
                    }
                })
            },
            openDialog(id, index) {
                this.dialog = true
                this.current_id = id
                this.current_index = index
            }
        }
    }
</script>

<style scoped>
    .block1 {
        padding: 50px 0;
    }

    a {
        text-decoration: none;
    }

    .block2__flex {
        margin-top: 50px;
        display: flex;
        flex-flow: row wrap;
        justify-content: space-between;
    }

    .block2__item {
        width: 540px;
        display: flex;
        flex-flow: row wrap;
        justify-content: flex-start;
        align-items: flex-start;
        transition: all .3s;
        margin-bottom: 50px;
    }

    .block2__img {
        width: 250px;
        height: 180px;
        -webkit-background-size: cover;
        background-size: cover;
        background-position: 50% 50%;
        margin-right: 30px;
    }

    .block2__text {
        width: 260px;
        position: relative;
        height: 180px;
    }

    .block2__text .h3 {
        font-weight: 500;
        font-size: 20px;
        text-decoration: none;
        color: #000000;
        display: block;
    }

    .edit {
        position: absolute;
        bottom: 5px;
        right: 55px;
        transition: all .3s;
        opacity: 0;
    }

    .delete {
        position: absolute;
        bottom: 5px;
        right: 5px;
        transition: all .3s;
        opacity: 0;
    }

    .block2__item .block2__text .h3:hover {
        color: #3f51b5;
        text-decoration: underline;
    }

    .block2__item:hover .edit, .block2__item:hover .delete {
        opacity: 1;
    }

    .block2__text .h3 span {
        color: #3f51b5;
    }

    .block2__text p {
        margin-top: 5px;
        color: #000000;
        opacity: .7;
    }

    .block2__text .category {
        color: #000000;
        opacity: .7;
        font-style: italic;
    }

    .block2__text .date {
        color: #000000;
        opacity: .7;
        position: absolute;
        bottom: 0;
        left: 0;
    }

    @media only screen and (max-width: 564px) {
        .block2__item {
            width: 100%;
        }
        .block2__img {
            margin-right: 0;
            width: 100%;
            height: 250px;
            margin-bottom: 20px;
        }
        .block2__text {
            width: 100%;
            height: auto;
        }
        .block2__text .date {
            position: static;
        }
        .delete {
            opacity: 1;
            top: -70px;
            right: 10px;
            bottom: auto;
        }
        .edit {
            opacity: 1;
            right: 10px;
            bottom: auto;
            top: -120px;
        }
    }
</style>