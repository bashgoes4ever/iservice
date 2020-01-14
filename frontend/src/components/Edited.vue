<template>
    <v-container>
        <div class="block1">
            <p>Объявление успешно изменено и ждет проверки модератором.</p>
            <router-link to="/">На главную</router-link>
        </div>
    </v-container>
</template>

<script>
    export default {
        name: "Edited"
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