<template>
    <v-container>
        <div class="block1">
            <h1>Редактирование объявления</h1>
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
            <div class="images__flex">
                <div class="image-item" v-for="(image, i) in images_old" :key="i">
                    <div class="image-wrap2"
                         :style="`background-image: url(http://178.21.8.217/${image.image_thumb})`"
                    ></div>
                    <div class="image-item-right">
                        <v-checkbox
                                class="image2-checkbox"
                                label="Главное изображение"
                                v-model="image.is_main"
                                :name="`old_is_main${i}`"
                        ></v-checkbox>
                        <v-checkbox
                                class="image2-checkbox"
                                label="Удалить?"
                                :name="`old_is_delete${i}`"
                        ></v-checkbox>
                    </div>
                </div>
            </div>
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
            <v-btn depressed color="indigo" class="white--text big-btn" @click="updateAdvert(advert_id)">Изменить</v-btn>
        </div>
    </v-container>
</template>

<script>
    import $ from 'jquery'
    import moment from 'moment'

    export default {
        name: "AdvertEdit",
        data: () => ({
            advert_id: 0,
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
            imei: '',
            images_old: [],
        }),
        created: function () {
            this.getCategories()
            this.getAdvert(this.$route.params.id)
            this.getPhone(this.$route.params.id)
        },
        methods: {
            getAdvert(page_id) {
                $.ajax({
                    url: `http://178.21.8.217/api/v1/adverts/${page_id}`,
                    type: 'GET',
                    success: (data) => {
                        this.advert_id = data.id
                        this.title = data.title
                        this.description = data.description
                        this.phone = data.phone
                        this.imei = data.imei
                        this.price = data.price
                        this.current_category = data.category.name
                        this.current_product = data.product.name
                        this.images_old = data.images
                    }
                })
            },
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
            formatDate(date) {
                return moment(date).format('DD.MM.YYYY')
            },
            getPhone(page_id) {
                $.ajax({
                    url: `http://178.21.8.217/api/v1/phone/${page_id}`,
                    type: 'GET',
                    success: (data) => {
                        this.phone = data.phone
                    }
                })
            },
            updateAdvert(advert_id) {
                var data = new FormData
                data.append('current_category', this.current_category)
                data.append('current_product', this.current_product)
                data.append('title', this.title)
                data.append('description', this.description)
                data.append('price', this.price)
                data.append('phone', this.phone)
                data.append('imei', this.imei)
                data.append('images_old', this.images_old.length)

                for (let i = 0; i < this.images_old.length; i++) {
                    data.append(`old_image${i}`, this.images_old[i].id)
                    if ($('input[name="old_is_main'+i+'"]').is(':checked')) {
                        data.append(`old_is_main${i}`, 'true')
                    } else {
                        data.append(`old_is_main${i}`, 'false')
                    }
                    if ($('input[name="old_is_delete'+i+'"]').is(':checked')) {
                        data.append(`old_is_delete${i}`, 'true')
                    } else {
                        data.append(`old_is_delete${i}`, 'false')
                    }
                }

                for (let i = 1; i <= this.images; i++) {
                    data.append(`image${i}`, $('input[name="image'+i+'"]').prop('files')[0])
                    if ($('input[name="is_main'+i+'"]').is(':checked')) {
                        data.append(`is_main${i}`, 'true')
                    } else {
                        data.append(`is_main${i}`, 'false')
                    }
                }
                $.ajax({
                    url: `http://178.21.8.217/api/v1/update_advert/${advert_id}`,
                    type: 'PUT',
                    data: data,
                    cache: false,
                    contentType: false,
                    processData: false,
                    success: () => {
                        this.$router.push('/edited')
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

    .images__flex {
        display: flex;
        flex-flow: row wrap;
        justify-content: flex-start;
        margin-bottom: 40px;
    }

    .image-wrap2 {
        width: 250px;
        height: 200px;
        -webkit-background-size: cover;
        background-size: cover;
        background-position: 50% 50%;
        position: relative;
        margin-right: 30px;
    }

    .image-wrap2 .delete {
        position: absolute;
        top: 10px;
        right: 10px;
        opacity: 0;
        transition: all .3s;
    }

    .image-wrap2:hover .delete {
        opacity: 1;
    }

    .image-item {
        width: 540px;
        margin-bottom: 40px;
        display: flex;
        flex-flow: row wrap;
        justify-content: flex-start;
    }
    .image-item-right {
        width: 200px;
    }
    .image2-checkbox {
        display: block;
        margin-top: 0 !important;
        padding-top: 0 !important;
    }

    @media only screen and (max-width: 564px) {
        .image-item {
            width: 100%;
        }
        .image-wrap2 {
            width: 100%;
            height: 250px;
            margin-right: 0;
            margin-bottom: 10px;
        }
        .image2-checkbox {
            margin-bottom: -10px;
        }
        .images__flex {
            margin-bottom: 0;
        }
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