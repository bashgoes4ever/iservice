<template>
    <v-container>
        <div class="block1">
            <h1>Создание объявления</h1>
            <v-select
                    :items="categories"
                    label="Категория"
                    name="category"
                    class="block2__select"
                    outlined
                    v-model="current_category"
            ></v-select>
            <v-select
                    :items="getProducts(current_category)"
                    label="Подкатегория"
                    name="product"
                    class="block2__select"
                    outlined
                    v-model="current_product"
            ></v-select>
            <v-text-field
                    label="Заголовок объявления"
                    name="title"
                    type="text"
                    :rules="titleRules"
                    v-model="title"
                    :counter="64"
                    outlined
            />
            <v-textarea
                    outlined
                    name="description"
                    label="Текст объявления"
                    :rules="descriptionRules"
                    v-model="description"
                    :counter="512"
            ></v-textarea>
            <v-text-field
                    label="Цена"
                    name="price"
                    type="number"
                    v-model="price"
                    outlined
            />
            <v-text-field
                    label="IMEI"
                    name="imei"
                    type="text"
                    v-model="imei"
                    outlined
            />
            <v-text-field
                    label="Телефон для связи"
                    name="phone"
                    type="text"
                    v-model="phone"
                    outlined
            />
            <h3>Фото:</h3>
            <div class="image-wrap" v-for="(image, i) in images" :key="i">
                <v-file-input
                        :rules="rules"
                        accept="image/png, image/jpeg, image/bmp"
                        placeholder="Выбрать фото"
                        prepend-icon="mdi-camera"
                        label="Фото"
                        class="file"
                        outlined
                        :name="`image${image}`"
                ></v-file-input>
                <v-checkbox
                        class="image-checkbox"
                        label="Главное изображение"
                        value="true"
                        :name="`is_main${image}`"
                ></v-checkbox>
            </div>
            <v-btn class="add-image" fab dark color="indigo" @click="addImage">
                <v-icon dark>mdi-plus</v-icon>
            </v-btn>
            <v-btn depressed color="indigo" class="white--text big-btn" @click="postAdvert">Подать объявление</v-btn>
        </div>
    </v-container>
</template>

<script>
    import $ from 'jquery'

    export default {
        name: "Apply",
        data: () => ({
            categories_raw: [],
            categories: [],
            current_category: '',
            current_product: '',
            phone: '',
            user_id: '',
            rules: [
                value => !value || value.size < 2000000 || 'Размер изображения не должен превышать 2 MB!',
            ],
            titleRules: [
                v => !!v || 'Введите заголовок!',
                v => v.length <= 64 || 'Заголовок не должен превышать 64 символа.',
            ],
            descriptionRules: [
                v => v.length <= 512 || 'Описание не должно превышать 512 символа.',
            ],
            images: 1,
            title: '',
            description: '',
            price: '',
            imei: ''
        }),
        created: function () {
            if (sessionStorage.getItem("auth_token")) {
                $.ajaxSetup({
                    headers: {'Authorization': "Token " + sessionStorage.getItem('auth_token')},
                });
            }
            this.getCategories()
            this.getUser()
        },
        methods: {
            addImage() {
                this.images++
            },
            getCategories() {
                $.ajax({
                    url: 'http://178.21.8.217/api/v1/categories/',
                    type: 'GET',
                    success: (data) => {
                        this.categories_raw = data
                        for (let i = 0; i < this.categories_raw.length; i++) {
                            this.categories.push(this.categories_raw[i]['name'])
                        }
                    }
                })
            },
            getProducts(category) {
                if (category == '') return []
                let result = this.categories_raw.find(obj => {
                    return obj.name === category
                })
                var temp = []
                for (let i = 0; i < result.products.length; i++) {
                    temp.push(result.products[i].name)
                }
                return temp
            },
            getUser() {
                $.ajax({
                    url: 'http://178.21.8.217/auth/users/me/',
                    type: 'GET',
                    success: (data) => {
                        this.phone = data.username
                        this.user_id = data.id
                    }
                })
            },
            postAdvert() {
                var data = new FormData
                data.append('current_category', this.current_category)
                data.append('current_product', this.current_product)
                data.append('title', this.title)
                data.append('description', this.description)
                data.append('price', this.price)
                data.append('phone', this.phone)
                data.append('imei', this.imei)
                data.append('user_id', this.user_id)
                for (let i = 1; i <= this.images; i++) {
                    data.append(`image${i}`, $('input[name="image'+i+'"]').prop('files')[0])
                    if ($('input[name="is_main'+i+'"]').is(':checked')) {
                        data.append(`is_main${i}`, 'true')
                    } else {
                        data.append(`is_main${i}`, 'false')
                    }
                }
                $.ajax({
                    url: 'http://178.21.8.217/api/v1/adverts/',
                    type: 'POST',
                    data: data,
                    cache: false,
                    contentType: false,
                    processData: false,
                    success: () => {
                        this.$router.push('/added')
                    }
                })
            }
        }
    }
</script>

<style scoped>
    .block1 {
        padding: 50px 0;
    }

    h1 {
        margin-bottom: 50px;
    }

    h3 {
        margin-bottom: 30px;
    }

    .image-wrap {
        display: flex;
        flex-flow: row wrap;
        justify-content: flex-start;
        align-items: flex-start;
    }

    .image-wrap .file {
        margin-right: 30px;
    }

    .image-checkbox {
        position: relative;
        top: -5px;
    }

    .add-image {
        margin: 0 auto;
        display: block;
    }

    .big-btn {
        width: 100%;
        height: 70px !important;
        margin-top: 50px;
    }

    @media only screen and (max-width: 460px) {
        .image-wrap .file {
            width: 100%;
            margin-right: 0;
            margin-bottom: -15px;
        }
        .image-checkbox {
            margin-top: 0;
            width: 100%;
        }
    }
</style>