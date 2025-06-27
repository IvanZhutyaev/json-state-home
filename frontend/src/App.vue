<script setup>
import Header from './components/Header.vue'
import HeroGallery from './components/HeroGallery.vue'
import Tour3D from './components/Tour3D.vue'
import { onMounted, onBeforeUnmount } from 'vue';
import { sendEvent } from './utils/analytics.js';

const apartmentId = 123; // Можно заменить на актуальный id
let startTime = 0;

onMounted(() => {
  startTime = Date.now();
});

onBeforeUnmount(() => {
  const duration = (Date.now() - startTime) / 1000;
  sendEvent(apartmentId, "time_on_page", duration);
});
</script>

<template>
  <div id="app">
    <Header />
    <HeroGallery />
    <Tour3D />
  </div>
</template>

<style scoped>
#app {
  margin: 0;
  padding: 0;
  font-weight: normal;
}
</style>
