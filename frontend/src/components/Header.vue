<template>
  <header class="header">
    <div class="header-container">
      <div class="logo">
        <img src="@/assets/logo.png" alt="Логотип" class="logo-img" />
        <span class="logo-text">Наш.Дом</span>
      </div>
      
      <nav class="nav">
        <a href="#" class="nav-link">Новостройки</a>
        <a href="#" class="nav-link">Застройщики</a>
        <a href="#" class="nav-link">Дома</a>
        <a href="#" class="nav-link">Управляющие компании</a>
        <a href="#" class="nav-link">Услуги</a>
      </nav>
      
      <div class="auth">
        <button class="btn-login" @click="openLoginModal">
          Войти
        </button>
      </div>
    </div>
    
    <!-- Модальное окно входа -->
    <LoginModal 
      :is-open="isLoginModalOpen" 
      @close="closeLoginModal" 
    />
  </header>
</template>

<script setup>
import { ref } from 'vue'
import LoginModal from './LoginModal.vue'

const isLoginModalOpen = ref(false)

const openLoginModal = () => {
  isLoginModalOpen.value = true
}

const closeLoginModal = () => {
  isLoginModalOpen.value = false
}
</script>

<style scoped>
.header {
  background: #fff;
  box-shadow: 0 2px 8px rgba(0, 122, 255, 0.15);
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
}

.header-container {
  max-width: 1280px;
  margin: 0 auto;
  padding: 0 2rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 70px;
}

.logo {
  display: flex;
  align-items: center;
  gap: 12px;
}

.logo-img {
  width: 40px;
  height: 40px;
}

.logo-text {
  font-size: 1.5rem;
  font-weight: 600;
  color: #007aff;
}

.nav {
  display: flex;
  gap: 2rem;
}

.nav-link {
  text-decoration: none;
  color: #2c3e50;
  font-weight: 500;
  transition: all 0.3s ease;
  padding: 8px 12px;
  border-radius: 6px;
}

.nav-link:hover {
  color: #007aff;
  background: rgba(0, 122, 255, 0.1);
}

.btn-login {
  background: #007aff;
  color: white;
  border: none;
  padding: 10px 24px;
  border-radius: 6px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.btn-login:hover {
  background: #0056cc;
}

@media (max-width: 768px) {
  .header-container {
    padding: 0 1rem;
  }
  
  .nav {
    display: none;
  }
  
  .logo-text {
    font-size: 1.2rem;
  }
}
</style> 