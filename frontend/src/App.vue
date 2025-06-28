<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue';
import { sendEvent } from './utils/analytics.js';
import Header from './components/Header.vue'
import HeroGallery from './components/HeroGallery.vue'

import UserDashboard from './components/UserDashboard.vue'
import DeveloperDashboard from './components/DeveloperDashboard.vue'
import MapYandex from './components/MapYandex.vue'

const apartmentId = 123; // Можно заменить на актуальный id
let startTime = 0;

// Состояние приложения
const currentView = ref('home') // 'home', 'user-dashboard', 'developer-dashboard'
const userType = ref(null) // 'user', 'developer'

onMounted(() => {
  startTime = Date.now();
  
  // Очищаем старые данные о текущем представлении
  localStorage.removeItem('currentView')
  
  // По умолчанию показываем главную страницу
  currentView.value = 'home'
  
  // Проверяем, есть ли сохраненный тип пользователя (только для данных пользователя)
  const savedUserType = localStorage.getItem('userType')
  
  if (savedUserType) {
    userType.value = savedUserType
  }
});

onBeforeUnmount(() => {
  const duration = (Date.now() - startTime) / 1000;
  sendEvent(apartmentId, "time_on_page", duration);
});

// Методы для переключения между представлениями
const showHome = () => {
  currentView.value = 'home'
}

const showUserDashboard = () => {
  currentView.value = 'user-dashboard'
  userType.value = 'user'
  localStorage.setItem('userType', 'user')
}

const showDeveloperDashboard = () => {
  currentView.value = 'developer-dashboard'
  userType.value = 'developer'
  localStorage.setItem('userType', 'developer')
}

const logout = () => {
  currentView.value = 'home'
  userType.value = null
  localStorage.removeItem('userType')
  localStorage.removeItem('userInfo')
}

const handleLoginSuccess = (userData) => {
  // Сохраняем информацию о пользователе
  localStorage.setItem('userInfo', JSON.stringify(userData))
  
  // НЕ переходим автоматически в личный кабинет
  // Пользователь остается на главной странице
  // Личный кабинет доступен через меню в хедере
}

const handleGoToDashboard = (userType) => {
  if (userType === 'user') {
    showUserDashboard()
  } else if (userType === 'developer') {
    showDeveloperDashboard()
  }
}

const handleGoHome = () => {
  showHome()
}
</script>

<template>
  <div id="app">
    <!-- Главная страница -->
    <div v-if="currentView === 'home'">
      <Header 
        @login-success="handleLoginSuccess"
        @go-to-dashboard="handleGoToDashboard"
        @go-home="handleGoHome"
        @logout="logout"
      />
      <HeroGallery />
      <MapYandex />

    </div>

    <!-- Личный кабинет пользователя -->
    <div v-else-if="currentView === 'user-dashboard'">
      <UserDashboard @logout="logout" @go-back="showHome" />
    </div>

    <!-- Личный кабинет застройщика -->
    <div v-else-if="currentView === 'developer-dashboard'">
      <DeveloperDashboard @logout="logout" @go-back="showHome" />
    </div>
  </div>
</template>

<style scoped>
#app {
  margin: 0;
  padding: 0;
  font-weight: normal;
}
</style>
