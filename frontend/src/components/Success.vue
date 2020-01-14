<template>
    <v-container>
        <div class="block1">
            <p>Объявление успешно добавлено и ждет проверки модератором.</p>
            <p>Вы можете отредактировать его в <router-link to="/my-adverts">личном кабинете</router-link></p>
            <router-link to="/">На главную</router-link>
        </div>
    </v-container>
</template>

<script>
    export default {
        name: "Success"
    }
</script>

<style scoped>
    p {
        margin-bottom: 5px;
    }
    .block1 {
        padding: 50px 0;
    }
</style>