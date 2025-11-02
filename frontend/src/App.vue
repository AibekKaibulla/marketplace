<template>
<div>
<NavBar />
<main class="container">
<router-view />
</main>
</div>
</template>


<script setup>
import NavBar from './components/NavBar.vue'
</script>


<style scoped>
.container { max-width: 900px; margin: 24px auto; padding: 0 16px; }
</style>