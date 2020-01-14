<template>
    <v-container>
        <div class="block1">
            <h1>Площадка объявлений <br>о продаже техники Apple, <br>запчастей и аксссесуаров к ней.</h1>
            <div class="block1__buttons">
                <v-btn depressed color="indigo" class="white--text" @click="slide_down('.block2')">Смотреть объявления
                </v-btn>
                <v-btn depressed outlined color="indigo" to="/apply">Подать объявление</v-btn>
            </div>
        </div>
        <v-divider></v-divider>
        <div class="block2">
            <div class="block2__filters">
                <!--<v-text-field-->
                <!--label="Что вы ищете?"-->
                <!--name="search"-->
                <!--prepend-inner-icon="mdi-magnify"-->
                <!--type="text"-->
                <!--outlined-->
                <!--clearable-->
                <!--/>-->
                <h2>Фильтры:</h2>
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
                <v-range-slider
                        v-model="range"
                        :max="max"
                        :min="min"
                        hide-details
                        class="align-center block2__slider"
                        label="Цена"
                        thumb-label
                        v-if="price_ready"
                ></v-range-slider>
                <v-btn
                        color="indigo"
                        class="white--text block2__button"
                        @click="getAdverts(1, current_category, current_product, range[1], range[0])"
                >Найти
                </v-btn>
                <v-btn text icon color="indigo"
                       class="block2__filter-none"
                       @click="filtersRefresh()">
                    <v-icon>mdi-close</v-icon>
                </v-btn>
            </div>
            <p v-if="adverts.length == 0 && !adverts_on_load">Объявлений пока нет.</p>
            <div class="block2__flex" v-if="adverts.length > 0 && !adverts_on_load">

                <router-link :to="`/adverts/${advert.id}`" class="block2__item" v-for="(advert, i) in adverts" :key="i">
                    <div class="block2__img"
                         v-if="advert.images.length > 0"
                         :style="`background-image: url(http://178.21.8.217/${getMainImage(advert.images)})`"></div>
                    <div class="block2__img"
                         v-else
                         style="background: #f0f0f0;"></div>
                    <div class="block2__text">
                        <h3>{{advert.title}} - <span>{{advert.price}} руб</span></h3>
                        <div class="category">Категория: {{advert.category.name}} {{advert.product.name}}</div>
                        <div class="date">{{formatDate(advert.created)}}</div>
                    </div>
                </router-link>

            </div>

            <div class="block10-load-wrapp load-wrapp" v-if="adverts_on_load">
                <div class="load-3">
                    <div class="line"></div>
                    <div class="line"></div>
                    <div class="line"></div>
                </div>
            </div>

            <v-btn
                    :loading="adverts_on_load"
                    :disabled="adverts_on_load"
                    color="indigo"
                    class="white--text load-button"
                    v-if="next_page && adverts.length > 0"
                    @click="getAdverts(next_page, current_category, current_product, range[1], range[0], true)"
            >
                Загрузить еще
                <v-icon right dark>mdi-cached</v-icon>
            </v-btn>
        </div>
    </v-container>
</template>

<script>
    import $ from 'jquery'
    import moment from 'moment'

    export default {
        name: 'Home',

        data: () => ({
            categories_raw: [],
            categories: [],
            current_category: '',
            current_product: '',
            range: [0, 0],
            min: 0,
            max: 0,
            price_ready: false,
            adverts_on_load: true,
            adverts: [],
            next_page: 1,
            load_on_cooldown: false
        }),
        computed: {},
        created: function () {
            this.getCategories()
            this.getAdverts(1)
            this.getPricesRange()
            window.addEventListener('scroll', this.loadContent)
        },
        destroyed: function () {
            window.removeEventListener('scroll', this.loadContent);
        },
        methods: {
            loadContent() {
                if (!this.load_on_cooldown && this.next_page != 0 && !this.adverts_on_load) {
                    var scroll_top = $(window).scrollTop() + $(window).height() + 300
                    var block2__bottom = $('.block2__flex').position().top + $('.block2__flex').height()
                    if (block2__bottom <= scroll_top) {
                        this.adverts_on_load = true
                        this.getAdverts(this.next_page, this.current_category, this.current_product, this.range[1], this.range[0], true)
                    }
                    this.load_on_cooldown = true
                    setTimeout(() => {
                        this.load_on_cooldown = false
                    }, 500)
                }
            },
            slide_down(select) {
                var destination = $(select).offset().top;
                $('html, body').animate({scrollTop: destination}, 500);
                return false;
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
            getAdverts(page, category = '', product = '', price__lte = '', price__gte = '', load_next = false) {
                this.adverts_on_load = true
                $.ajax({
                    url: `http://178.21.8.217/api/v1/adverts/?page=${page}&category=${category}&product=${product}&price__lte=${price__lte}&price__gte=${price__gte}`,
                    type: 'GET',
                    success: (data) => {
                        if (load_next) {
                            this.adverts = this.adverts.concat(data.data)
                        } else {
                            this.adverts = data.data
                        }
                        this.next_page = data.next_page
                        this.adverts_on_load = false
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
            getPricesRange() {
                $.ajax({
                    url: `http://178.21.8.217/api/v1/prices/`,
                    type: 'GET',
                    success: (data) => {
                        this.range[0] = data.min
                        this.range[1] = data.max
                        this.min = data.min
                        this.max = data.max
                        this.price_ready = true
                    }
                })
            },
            filtersRefresh() {
                this.price_ready = false
                this.current_category = ''
                this.current_product = ''
                this.range = [0, 0]
                this.min = 0
                this.max = 0
                this.getPricesRange()
                this.getAdverts(1)
            }
        }
    };
</script>

<style scoped>
    h1 {
        text-align: center;
    }

    .block1 {
        padding: 50px 0;
    }

    .block1__buttons {
        padding-top: 30px;
        text-align: center;
    }

    .block1__buttons button:first-child {
        margin-right: 20px;
    }

    .block2 {
        padding: 50px 0;
    }

    a {
        text-decoration: none;
    }

    .block2__flex {
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

    .block2__text h3 {
        font-weight: 500;
        font-size: 20px;
        text-decoration: none;
        color: #000000;
    }

    .block2__item:hover .block2__text h3 {
        color: #3f51b5;
        text-decoration: underline;
    }

    .block2__text h3 span {
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

    .load-button {
        display: block;
        margin: 0 auto;
    }

    .block2__filters {
        margin-bottom: 50px;
        display: flex;
        flex-flow: row wrap;
        justify-content: space-between;
        align-items: flex-start;
    }

    .block2__filters .v-input {
        width: 200px;
        margin-right: 20px;
    }

    .block2__filters .block2__select {
        width: 140px;
    }

    .block2__button, .block2__slider {
        margin-top: 10px;
    }

    .block2__filter-none {
        margin-top: 10px;
        margin-left: 10px;
    }

    .block2__filters h2 {
        margin-top: 10px;
        margin-right: 30px;
    }

    /* =loaders
    ---------------------- */
    .block2-load-wrapp {
        margin-top: 60px;
        min-height: 300px;
    }

    .block10-load-wrapp {
        min-height: 200px;
    }

    .products-empty {
        padding-top: 70px;
        text-align: center;
        font-size: 20px;
    }

    .load-wrapp {
        width: 100%;
        text-align: center;
        position: relative;
    }

    .load-3 {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
    }

    .load-wrapp p {
        padding: 0 0 20px;
    }

    .load-wrapp:last-child {
        margin-right: 0;
    }

    .line {
        display: inline-block;
        width: 15px;
        height: 15px;
        border-radius: 15px;
        background-color: #4b9cdb;
        margin-right: 5px;
    }

    .ring-1 {
        width: 10px;
        height: 10px;
        margin: 0 auto;
        padding: 10px;
        border: 7px dashed #4b9cdb;
        border-radius: 100%;
    }

    .ring-2 {
        position: relative;
        width: 45px;
        height: 45px;
        margin: 0 auto;
        border: 4px solid #4b9cdb;
        border-radius: 100%;
    }

    .ball-holder {
        position: absolute;
        width: 12px;
        height: 45px;
        left: 17px;
        top: 0px;
    }

    .ball {
        position: absolute;
        top: -11px;
        left: 0;
        width: 16px;
        height: 16px;
        border-radius: 100%;
        background: #4282B3;
    }

    .letter-holder {
        padding: 16px;
    }

    .letter {
        float: left;
        font-size: 14px;
        color: #777;
    }

    .square {
        width: 12px;
        height: 12px;
        border-radius: 4px;
        background-color: #4b9cdb;
    }

    .spinner {
        position: relative;
        width: 45px;
        height: 45px;
        margin: 0 auto;
    }

    .bubble-1,
    .bubble-2 {
        position: absolute;
        top: 0;
        width: 25px;
        height: 25px;
        border-radius: 100%;
        background-color: #4b9cdb;
    }

    .bubble-2 {
        top: auto;
        bottom: 0;
    }

    .bar {
        float: left;
        width: 15px;
        height: 6px;
        border-radius: 2px;
        background-color: #4b9cdb;
    }

    /* =Animate the stuff
    ------------------------ */
    .load-1 .line:nth-last-child(1) {
        animation: loadingA 1.5s 1s infinite;
    }

    .load-1 .line:nth-last-child(2) {
        animation: loadingA 1.5s .5s infinite;
    }

    .load-1 .line:nth-last-child(3) {
        animation: loadingA 1.5s 0s infinite;
    }

    .load-2 .line:nth-last-child(1) {
        animation: loadingB 1.5s 1s infinite;
    }

    .load-2 .line:nth-last-child(2) {
        animation: loadingB 1.5s .5s infinite;
    }

    .load-2 .line:nth-last-child(3) {
        animation: loadingB 1.5s 0s infinite;
    }

    .load-3 .line:nth-last-child(1) {
        animation: loadingC .6s .1s linear infinite;
    }

    .load-3 .line:nth-last-child(2) {
        animation: loadingC .6s .2s linear infinite;
    }

    .load-3 .line:nth-last-child(3) {
        animation: loadingC .6s .3s linear infinite;
    }

    .load-4 .ring-1 {
        animation: loadingD 1.5s .3s cubic-bezier(.17, .37, .43, .67) infinite;
    }

    .load-5 .ball-holder {
        animation: loadingE 1.3s linear infinite;
    }

    .load-6 .letter {
        animation-name: loadingF;
        animation-duration: 1.6s;
        animation-iteration-count: infinite;
        animation-direction: linear;
    }

    .l-1 {
        animation-delay: .48s;
    }

    .l-2 {
        animation-delay: .6s;
    }

    .l-3 {
        animation-delay: .72s;
    }

    .l-4 {
        animation-delay: .84s;
    }

    .l-5 {
        animation-delay: .96s;
    }

    .l-6 {
        animation-delay: 1.08s;
    }

    .l-7 {
        animation-delay: 1.2s;
    }

    .l-8 {
        animation-delay: 1.32s;
    }

    .l-9 {
        animation-delay: 1.44s;
    }

    .l-10 {
        animation-delay: 1.56s;
    }

    .load-7 .square {
        animation: loadingG 1.5s cubic-bezier(.17, .37, .43, .67) infinite;
    }

    .load-8 .line {
        animation: loadingH 1.5s cubic-bezier(.17, .37, .43, .67) infinite;
    }

    .load-9 .spinner {
        animation: loadingI 2s linear infinite;
    }

    .load-9 .bubble-1, .load-9 .bubble-2 {
        animation: bounce 2s ease-in-out infinite;
    }

    .load-9 .bubble-2 {
        animation-delay: -1.0s;
    }

    .load-10 .bar {
        animation: loadingJ 2s cubic-bezier(.17, .37, .43, .67) infinite;
    }

    @keyframes loadingA {

    0
    {
        height: 15px
    ;
    }
    50
    %
    {
        height: 35px
    ;
    }
    100
    %
    {
        height: 15px
    ;
    }
    }

    @keyframes loadingB {

    0
    {
        width: 15px
    ;
    }
    50
    %
    {
        width: 35px
    ;
    }
    100
    %
    {
        width: 15px
    ;
    }
    }

    @keyframes loadingC {

    0
    {
        transform: translate(0, 0)
    ;
    }
    50
    %
    {
        transform: translate(0, 15px)
    ;
    }
    100
    %
    {
        transform: translate(0, 0)
    ;
    }
    }

    @keyframes loadingD {

    0
    {
        transform: rotate(0deg)
    ;
    }
    50
    %
    {
        transform: rotate(180deg)
    ;
    }
    100
    %
    {
        transform: rotate(360deg)
    ;
    }
    }

    @keyframes loadingE {

    0
    {
        transform: rotate(0deg)
    ;
    }
    100
    %
    {
        transform: rotate(360deg)
    ;
    }
    }

    @keyframes loadingF {
        0% {
            opacity: 0;
        }
        100% {
            opacity: 1;
        }
    }

    @keyframes loadingG {
        0% {
            transform: translate(0, 0) rotate(0deg);
        }
        50% {
            transform: translate(70px, 0) rotate(360deg);
        }
        100% {
            transform: translate(0, 0) rotate(0deg);
        }
    }

    @keyframes loadingH {
        0% {
            width: 15px;
        }
        50% {
            width: 35px;
            padding: 4px;
        }
        100% {
            width: 15px;
        }
    }

    @keyframes loadingI {
        100% {
            transform: rotate(360deg);
        }
    }

    @keyframes bounce {
        0%, 100% {
            transform: scale(0.0);
        }
        50% {
            transform: scale(1.0);
        }
    }

    @keyframes loadingJ {
        0%, 100% {
            transform: translate(0, 0);
        }

        50% {
            transform: translate(80px, 0);
            background-color: #f5634a;
            width: 25px;
        }
    }

    @media only screen and (max-width: 840px) {
        .block2__filters h2 {
            width: 100%;
            margin-right: 0;
            margin-top: 0;
            margin-bottom: 20px;
        }
        .block2__item {
            width: 100%;
        }
        .block2__text {
            width: 340px;
        }
    }

    @media only screen and (max-width: 700px) {
        .block2__filters .block2__select {
            width: 40%;
        }
        .block2__filters .block2__select:nth-child(3) {
            margin-right: 0;
        }
        .block2__text {
            width: 260px;
        }
    }

    @media only screen and (max-width: 570px) {
        .block2__img {
            display: none;
        }
        .block2__item {
            border-bottom: 1px solid #eeeeee;
            padding-bottom: 20px;
            margin-bottom: 20px;
        }
        .block2__item:last-child {
            border-bottom: none;
        }
        .block2__text {
            width: 100%;
            height: auto;
        }
        .block2__text .date {
            position: static;
        }
        h1 {
            font-size: 26px;
            font-weight: 500;
        }
        h1 br {
            display: none;
        }
        .block1__buttons {
            display: flex;
            flex-flow: row wrap;
            justify-content: center;
        }
        .block1__buttons button, .block1__buttons a {
            width: 100%;
        }
        .block1__buttons button:first-child {
            margin-right: 0;
            margin-bottom: 10px;
        }
        .block2__filters .block2__select {
            width: 100%;
            margin-right: 0;
            margin-bottom: -10px;
        }
        .block2__filters .block2__slider {
            margin-right: 0;
            width: 100%;
            margin-bottom: 10px;
        }
    }
</style>
