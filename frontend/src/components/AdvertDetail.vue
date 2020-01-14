<template>
    <v-container>
        <div class="block1">
            <carousel
                class="slider"
                :responsiveClass="true"
                :addClassActive="true"
                :nav="true"
                :items="1"
                :navText="nav_text"
                v-if="advert_is_loaded && advert.images.length > 0"
            >
                <a
                        class="slide"
                        :data-lightbox="`product${i}`"
                        :href="`http://178.21.8.217/${image.image}`"
                        :style="`background-image: url(http://178.21.8.217/${image.image_thumb})`"
                        v-for="(image, i) in advert.images" :key="i"
                ></a>
            </carousel>

            <div class="block1__right">
                <h1>{{advert.title}}</h1>
                <p class="description">{{advert.description}}</p>
                <p class="price">Цена: {{advert.price}} рублей</p>
                <p class="imei" v-if="advert.imei">IMEI: {{advert.imei}}</p>
                <v-btn
                        color="indigo"
                        class="white--text block2__button"
                        @click="getPhone($route.params.id)"
                        v-if="!phone_is_loaded"
                >Показать контакты продавца</v-btn>
                <p class="phone indigo--text" v-if="phone_is_loaded">{{phone}}</p>
                <p class="category">Категория: {{advert.category.name}} {{advert.product.name}}</p>
                <p class="date">{{formatDate(advert.created)}}</p>
            </div>
        </div>
    </v-container>
</template>

<script>
    import $ from 'jquery'
    import 'lightbox2/dist/css/lightbox.min.css'
    import 'lightbox2/dist/js/lightbox.min'
    import carousel from 'vue-owl-carousel'
    import moment from 'moment'

    export default {
        name: "AdvertDetail",
        data: () => ({
            advert_is_loaded: false,
            advert: {},
            nav_text: ["<i aria-hidden='true' class='v-icon notranslate mdi mdi-chevron-left theme--light'></i>",
                "<i aria-hidden='true' class='v-icon notranslate mdi mdi-chevron-right theme--light'></i>"],
            phone: '',
            phone_is_loaded: false
        }),
        components: {carousel},
        created: function () {
            this.getAdvert(this.$route.params.id)
        },
        methods: {
            getAdvert(page_id) {
              $.ajax({
                    url: `http://178.21.8.217/api/v1/adverts/${page_id}`,
                    type: 'GET',
                    success: (data) => {
                        this.advert = data
                        this.advert_is_loaded = true
                    }
                })
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
                        this.phone_is_loaded = true
                    }
                })
            }
        }
    }
</script>

<style scoped>
    .block1 {
        display: flex;
        flex-flow: row wrap;
        justify-content: flex-start;
        padding: 50px 0;
    }
    .slider {
        width: 300px;
        height: 400px;
        margin-right: 50px;
    }
    .slide {
        display: block;
        width: 300px;
        height: 400px;
        -webkit-background-size: cover;
        background-size: cover;
        background-position: 50% 50%;
    }
    p {
        margin-bottom: 10px;
    }
    h1 {
        margin-bottom: 20px;
    }
    .category {
        margin-top: 10px;
        font-style: italic;
        opacity: .7;
    }
    .date {
        opacity: .7;
        position: absolute;
        bottom: 0;
        left: 0;
        margin-bottom: 0;
    }
    .block1__right {
        position: relative;
        min-height: 400px;
        padding-bottom: 50px;
        width: 800px;
    }
    .phone {
        font-size: 20px;
        font-weight: bold;
    }
    @media only screen and (max-width: 1270px) {
        .block1__right {
            width: 500px;
        }
    }
    @media only screen and (max-width: 880px) {
        .block1__right {
            width: 400px;
        }
        .slider {
            margin-right: 30px;
        }
    }
    @media only screen and (max-width: 755px) {
        .block1__right {
            width: 100%;
            padding: 0 12px;
            margin-top: 20px;
            height: auto;
        }
        .block1__right .date {
            position: static;
        }
        .slider {
            width: 100%;
            margin-right: 0;
            height: 300px;
        }
        .slide {
            width: 100%;
            height: 300px;
        }
        .container {
            padding: 0;
        }
        .block1 {
            padding: 0;
        }
    }
</style>

<style>

    .owl-dots {
        display: none;
    }
    .owl-theme .owl-nav .owl-prev, .owl-theme .owl-nav .owl-next {
        position: absolute;
        top: 50%;
        -webkit-transform: translateY(-50%);
        -moz-transform: translateY(-50%);
        -ms-transform: translateY(-50%);
        -o-transform: translateY(-50%);
        transform: translateY(-50%);
        background: transparent;
        padding: 0;
        margin: 0;
    }
    .owl-theme .owl-nav .owl-prev:hover, .owl-theme .owl-nav .owl-next:hover {
        background: transparent;
        opacity: .7;
    }
    .owl-theme .owl-nav .owl-prev i, .owl-theme .owl-nav .owl-next i {
        color: #ffffff;
        font-size: 50px;
    }
    .owl-theme .owl-nav .owl-prev {
        left: 0;
    }
    .owl-theme .owl-nav .owl-next {
        right: 0;
    }
</style>