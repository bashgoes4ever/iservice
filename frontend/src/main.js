import Vue from 'vue'
import App from './App.vue'
import vuetify from './plugins/vuetify';
import VueRouter from 'vue-router'
import Home from './components/Home'
import Registration from './components/Registration'
import Login from './components/Login'
import AdvertDetail from './components/AdvertDetail'
import Apply from './components/Apply'
import Success from './components/Success'
import MyAdverts from './components/MyAdverts'
import AdvertEdit from './components/AdvertEdit'
import Edited from './components/Edited'

Vue.config.productionTip = false

Vue.use(VueRouter)

const routes = [
    {
        path: '/',
        component: Home,
        name: 'home',
        meta: {
            title: 'Главная'
        }
    },
    {
        path: '/registration',
        component: Registration,
        name: 'registration',
        meta: {
            title: 'Регистрация'
        }
    },
    {
        path: '/login',
        component: Login,
        name: 'login',
        meta: {
            title: 'Вход'
        }
    },
    {
        path: '/adverts/:id',
        component: AdvertDetail,
        name: 'advert_detail',
        meta: {
            title: 'Объявление'
        }
    },
    {
        path: '/apply',
        component: Apply,
        name: 'apply',
        meta: {
            title: 'Создать объявление',
            auth: true
        }
    },
    {
        path: '/added',
        component: Success,
        name: 'added',
        meta: {
            title: 'Объявление успешно добавлено'
        }
    },
    {
        path: '/my-adverts',
        component: MyAdverts,
        name: 'my-adverts',
        meta: {
            title: 'Мои объявления',
            auth: true
        }
    },
    {
        path: '/my-adverts/:id',
        component: AdvertEdit,
        name: 'advert_edit',
        meta: {
            title: 'Редактирование объявления',
            auth: true
        }
    },
    {
        path: '/edited',
        component: Edited,
        name: 'edited',
        meta: {
            title: 'Объявление успешно изменено'
        }
    },
]

const router = new VueRouter({
    routes,
    mode: 'history',
    scrollBehavior() {
        return {x: 0, y: 0}
    }
})

router.beforeEach((to, from, next) => {
    if (to.meta.auth == true && !sessionStorage.getItem("auth_token")) {
        router.push('/registration')
    } else {
        document.title = to.meta.title
        next()
    }
})

new Vue({
    router,
    vuetify,
    render: h => h(App)
}).$mount('#app')