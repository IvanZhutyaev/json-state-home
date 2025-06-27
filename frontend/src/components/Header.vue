<template>
  <header class="header">
    <div class="header-container">
      <div class="logo" @click="goHome">
        <img src="@/assets/logo.svg" alt="Логотип" class="logo-img" />
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
        <div v-if="isLoggedIn" class="user-menu">
          <button class="user-btn" @click="toggleUserMenu">
            <span class="user-status-indicator"></span>
            {{ userInfo.name }}
            <span class="user-icon">▼</span>
          </button>
          <div v-if="showUserMenu" class="user-dropdown">
            <button class="dropdown-item" @click="goToDashboard">
              Личный кабинет
            </button>
            <button class="dropdown-item" @click="logout">
              Выйти
            </button>
          </div>
        </div>
        <button v-else class="btn-login" @click="openLoginModal">
          Войти
        </button>
      </div>
    </div>
    
    <!-- Модальное окно входа -->
    <LoginModal 
      :is-open="isLoginModalOpen" 
      @close="closeLoginModal"
      @login-success="handleLoginSuccess"
    />
  </header>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import LoginModal from './LoginModal.vue'

const emit = defineEmits(['login-success', 'go-to-dashboard', 'go-home', 'logout'])

const isLoginModalOpen = ref(false)
const isLoggedIn = ref(false)
const showUserMenu = ref(false)
const userInfo = ref({
  name: 'Пользователь',
  type: null
})

const openLoginModal = () => {
  isLoginModalOpen.value = true
}

const closeLoginModal = () => {
  isLoginModalOpen.value = false
}

const handleLoginSuccess = (userData) => {
  isLoggedIn.value = true
  userInfo.value = {
    name: userData.name || 'Пользователь',
    type: userData.type
  }
  closeLoginModal()
  
  // Сохраняем информацию о пользователе в localStorage
  localStorage.setItem('userInfo', JSON.stringify(userInfo.value))
  
  // Эмитим событие для родительского компонента
  emit('login-success', userData)
}

const toggleUserMenu = () => {
  showUserMenu.value = !showUserMenu.value
}

const goToDashboard = () => {
  showUserMenu.value = false
  // Переход к личному кабинету будет обработан в родительском компоненте
  emit('go-to-dashboard', userInfo.value.type)
}

const logout = () => {
  isLoggedIn.value = false
  userInfo.value = { name: 'Пользователь', type: null }
  showUserMenu.value = false
  
  // Очищаем данные из localStorage
  localStorage.removeItem('userInfo')
  localStorage.removeItem('userType')
  
  emit('logout')
}

const goHome = () => {
  emit('go-home')
}

onMounted(() => {
  // Проверяем, есть ли сохраненные данные пользователя
  const savedUser = localStorage.getItem('userInfo')
  if (savedUser) {
    const user = JSON.parse(savedUser)
    isLoggedIn.value = true
    userInfo.value = user
  }
})
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
  cursor: pointer;
  transition: opacity 0.2s;
}

.logo:hover {
  opacity: 0.8;
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

.auth {
  position: relative;
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

.user-menu {
  position: relative;
}

.user-btn {
  background: #f5f5f5;
  color: #2c3e50;
  border: none;
  padding: 10px 16px;
  border-radius: 6px;
  font-weight: 500;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.3s ease;
  animation: slideIn 0.3s ease;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.user-icon {
  font-size: 0.8rem;
  transition: transform 0.2s;
}

.user-dropdown {
  position: absolute;
  top: 100%;
  right: 0;
  background: white;
  border: 1px solid #eee;
  border-radius: 6px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  min-width: 150px;
  z-index: 1001;
  margin-top: 4px;
}

.dropdown-item {
  display: block;
  width: 100%;
  padding: 10px 16px;
  border: none;
  background: none;
  text-align: left;
  cursor: pointer;
  transition: background-color 0.2s;
  color: #2c3e50;
}

.dropdown-item:hover {
  background: #f5f5f5;
}

.dropdown-item:first-child {
  border-radius: 6px 6px 0 0;
}

.dropdown-item:last-child {
  border-radius: 0 0 6px 6px;
}

.user-btn:hover {
  background: #e5e5e5;
}

.user-status-indicator {
  width: 8px;
  height: 8px;
  background: #34c759;
  border-radius: 50%;
  margin-right: 4px;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0% {
    box-shadow: 0 0 0 0 rgba(52, 199, 89, 0.7);
  }
  70% {
    box-shadow: 0 0 0 6px rgba(52, 199, 89, 0);
  }
  100% {
    box-shadow: 0 0 0 0 rgba(52, 199, 89, 0);
  }
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