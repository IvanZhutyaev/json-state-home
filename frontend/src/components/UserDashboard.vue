<template>
  <div class="dashboard-container">
    <div class="dashboard-header">
      <h1>Личный кабинет</h1>
      <div class="header-actions">
        <button class="back-btn" @click="goBack">← Вернуться</button>
        <button class="logout-btn" @click="logout">Выйти</button>
      </div>
    </div>

    <div class="dashboard-content">
      <!-- Индикатор загрузки -->
      <div v-if="loading" class="loading-indicator">
        <div class="loading-spinner"></div>
        <p>Загрузка данных...</p>
      </div>

      <!-- Личная информация -->
      <div v-else class="dashboard-section">
        <h2>Личная информация</h2>
        <div class="user-info">
          <div class="info-item">
            <label>Имя:</label>
            <span>{{ userInfo.name }}</span>
          </div>
          <div class="info-item">
            <label>Телефон:</label>
            <span>{{ userInfo.phone }}</span>
          </div>
          <button class="edit-btn" @click="editProfile">Редактировать</button>
        </div>
      </div>

      <!-- Забронированные объекты -->
      <div v-if="!loading" class="dashboard-section">
        <h2>Забронированные объекты</h2>
        <div v-if="bookedProperties.length === 0" class="empty-state">
          <p>У вас пока нет забронированных объектов</p>
          <button class="browse-btn" @click="browseProperties">Найти недвижимость</button>
        </div>
        <div v-else class="properties-grid">
          <div 
            v-for="property in bookedProperties" 
            :key="property.id"
            class="property-card"
          >
            <div class="property-image">
              <img :src="property.image" :alt="property.name" />
              <div class="property-status booked">Забронировано</div>
            </div>
            <div class="property-info">
              <h3>{{ property.name }}</h3>
              <p class="property-address">{{ property.address }}</p>
              <p class="property-price">{{ property.price }} ₽</p>
              <div class="property-actions">
                <button class="action-btn primary" @click="buyProperty(property.id)">
                  Купить
                </button>
                <button class="action-btn secondary" @click="cancelBooking(property.id)">
                  Отменить бронь
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Поиск недвижимости -->
      <div v-if="!loading" class="dashboard-section">
        <h2>Найти недвижимость</h2>
        <div class="search-filters">
          <div class="filter-group">
            <label>Город:</label>
            <input v-model="searchFilters.city" placeholder="Введите город" />
          </div>
          <div class="filter-group">
            <label>Цена от:</label>
            <input v-model="searchFilters.minPrice" type="number" placeholder="0" />
          </div>
          <div class="filter-group">
            <label>Цена до:</label>
            <input v-model="searchFilters.maxPrice" type="number" placeholder="10000000" />
          </div>
          <div class="filter-group">
            <label>Количество комнат:</label>
            <select v-model="searchFilters.rooms">
              <option value="">Любое</option>
              <option value="1">1</option>
              <option value="2">2</option>
              <option value="3">3</option>
              <option value="4">4+</option>
            </select>
          </div>
          <div class="filter-group">
            <label>Площадь от (м²):</label>
            <input v-model="searchFilters.minArea" type="number" placeholder="0" />
          </div>
          <div class="filter-group">
            <label>Площадь до (м²):</label>
            <input v-model="searchFilters.maxArea" type="number" placeholder="200" />
          </div>
          <button class="search-btn" @click="searchProperties">Найти</button>
          <button class="clear-btn" @click="clearFilters">Очистить</button>
        </div>

        <div v-if="searchResults.length > 0" class="search-results">
          <h3>Результаты поиска</h3>
          <div class="properties-grid">
            <div 
              v-for="property in searchResults" 
              :key="property.id"
              class="property-card"
            >
              <div class="property-image">
                <img :src="property.image" :alt="property.name" />
                <div class="property-status available">Доступно</div>
              </div>
              <div class="property-info">
                <h3>{{ property.name }}</h3>
                <p class="property-address">{{ property.address }}</p>
                <p class="property-price">{{ property.price }} ₽</p>
                <div class="property-actions">
                  <button class="action-btn primary" @click="bookProperty(property.id)">
                    Забронировать
                  </button>
                  <button class="action-btn secondary" @click="viewDetails(property.id)">
                    Подробнее
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Модальное окно редактирования профиля -->
    <div v-if="showEditModal" class="modal-overlay" @click="closeEditModal">
      <div class="modal-content" @click.stop>
        <h3>Редактировать профиль</h3>
        <div class="form-group">
          <label>Имя:</label>
          <input v-model="editForm.name" type="text" />
        </div>
        <div class="form-group">
          <label>Телефон:</label>
          <input v-model="editForm.phone" type="tel" />
        </div>
        <div class="modal-actions">
          <button class="btn-secondary" @click="closeEditModal">Отмена</button>
          <button class="btn-primary" @click="saveProfile">Сохранить</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { userAPI, propertyAPI } from '../utils/api.js'
import analytics from '../utils/analytics.js'

const emit = defineEmits(['logout', 'go-back'])

// Данные пользователя
const userInfo = ref({
  name: '',
  phone: ''
})

// Забронированные объекты
const bookedProperties = ref([])

// Поиск недвижимости
const searchFilters = reactive({
  city: '',
  minPrice: '',
  maxPrice: '',
  rooms: '',
  minArea: '',
  maxArea: ''
})

const searchResults = ref([])

// Модальное окно редактирования
const showEditModal = ref(false)
const editForm = reactive({
  name: '',
  phone: ''
})

// Загрузка данных пользователя
const loading = ref(false)

const loadUserData = async () => {
  loading.value = true
  try {
    // Получаем ID пользователя из localStorage или используем первый доступный
    let userId = 1
    
    // Попробуем получить из localStorage (если пользователь авторизован)
    const userInfoRaw = localStorage.getItem('userInfo')
    if (userInfoRaw) {
      const userData = JSON.parse(userInfoRaw)
      if (userData.type === 'user' && userData.id) {
        userId = userData.id
      }
    }
    
    // Загружаем информацию о пользователе
    const user = await userAPI.getUser(userId)
    userInfo.value = {
      name: user.User_name,
      phone: user.Phone_number || 'Не указан'
    }
    
    // Загружаем забронированные объекты
    const bookings = await propertyAPI.getUserBookings(userId)
    bookedProperties.value = bookings.map(booking => ({
      id: booking.property.id,
      name: booking.property.name,
      address: booking.property.address,
      price: booking.property.price.toLocaleString(),
      image: booking.property.image_url || 'https://via.placeholder.com/300x200/007aff/ffffff?text=Недвижимость'
    }))
    
  } catch (error) {
    console.error('Ошибка загрузки данных пользователя:', error)
    alert('Ошибка загрузки данных. Проверьте подключение к серверу.')
  } finally {
    loading.value = false
  }
}

// Методы
const logout = () => {
  // Эмитим событие для родительского компонента
  emit('logout')
}

const goBack = () => {
  // Эмитим событие для возврата на главную страницу
  emit('go-back')
}

const editProfile = () => {
  editForm.name = userInfo.value.name
  editForm.phone = userInfo.value.phone
  showEditModal.value = true
}

const closeEditModal = () => {
  showEditModal.value = false
}

const saveProfile = async () => {
  try {
    // Получаем ID пользователя
    let userId = 1
    const userInfoRaw = localStorage.getItem('userInfo')
    if (userInfoRaw) {
      const userData = JSON.parse(userInfoRaw)
      if (userData.type === 'user' && userData.id) {
        userId = userData.id
      }
    }
    
    await userAPI.updateProfile(userId, editForm.name, editForm.phone)
    userInfo.value.name = editForm.name
    userInfo.value.phone = editForm.phone
    closeEditModal()
    alert('Профиль успешно обновлен!')
  } catch (error) {
    console.error('Ошибка обновления профиля:', error)
    alert('Ошибка при обновлении профиля')
  }
}

const browseProperties = () => {
  // Переход к поиску недвижимости
  console.log('Поиск недвижимости')
}

const searchProperties = async () => {
  try {
    // Отслеживаем поиск
    analytics.trackSearch(searchFilters)
    
    const results = await propertyAPI.searchProperties(searchFilters)
    searchResults.value = results.map(property => ({
      id: property.id,
      name: property.name,
      address: property.address,
      price: property.price.toLocaleString(),
      image: property.image_url || 'https://via.placeholder.com/300x200/007aff/ffffff?text=Недвижимость'
    }))
  } catch (error) {
    console.error('Ошибка поиска недвижимости:', error)
  }
}

const bookProperty = async (propertyId) => {
  try {
    // Отслеживаем клик по бронированию
    analytics.trackBookClick(propertyId)
    
    // Получаем ID пользователя
    let userId = 1
    const userInfoRaw = localStorage.getItem('userInfo')
    if (userInfoRaw) {
      const userData = JSON.parse(userInfoRaw)
      if (userData.type === 'user' && userData.id) {
        userId = userData.id
      }
    }
    
    await propertyAPI.bookProperty(propertyId, userId)
    alert('Недвижимость забронирована!')
    // Перезагружаем данные
    await loadUserData()
  } catch (error) {
    console.error('Ошибка бронирования:', error)
    alert('Ошибка при бронировании')
  }
}

const buyProperty = async (propertyId) => {
  try {
    // Получаем ID пользователя
    let userId = 1
    const userInfoRaw = localStorage.getItem('userInfo')
    if (userInfoRaw) {
      const userData = JSON.parse(userInfoRaw)
      if (userData.type === 'user' && userData.id) {
        userId = userData.id
      }
    }
    
    await propertyAPI.purchaseProperty(propertyId, userId)
    alert('Недвижимость куплена!')
    // Перезагружаем данные
    await loadUserData()
  } catch (error) {
    console.error('Ошибка покупки:', error)
    alert('Ошибка при покупке')
  }
}

const cancelBooking = (propertyId) => {
  // Логика отмены брони
  console.log('Отмена брони:', propertyId)
}

const viewDetails = (propertyId) => {
  // Отслеживаем просмотр деталей квартиры
  analytics.trackApartmentView(propertyId)
  
  // Просмотр деталей объекта
  console.log('Детали объекта:', propertyId)
}

const clearFilters = () => {
  // Отслеживаем очистку фильтров
  analytics.trackFilterApplied(0)
  
  // Логика очистки фильтров
  searchFilters.city = ''
  searchFilters.minPrice = ''
  searchFilters.maxPrice = ''
  searchFilters.rooms = ''
  searchFilters.minArea = ''
  searchFilters.maxArea = ''
}

onMounted(() => {
  console.log('Загрузка данных пользователя')
  loadUserData()
})
</script>

<style scoped>
.dashboard-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 2px solid #007aff;
}

.dashboard-header h1 {
  color: #007aff;
  margin: 0;
}

.header-actions {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.back-btn {
  background: #f5f5f5;
  color: #2c3e50;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 500;
  transition: background-color 0.3s ease;
}

.back-btn:hover {
  background: #e5e5e5;
}

.logout-btn {
  background: #ff3b30;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 500;
}

.logout-btn:hover {
  background: #d70015;
}

.dashboard-section {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  margin-bottom: 2rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.dashboard-section h2 {
  color: #2c3e50;
  margin-bottom: 1.5rem;
  font-size: 1.5rem;
}

.user-info {
  display: grid;
  gap: 1rem;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.info-item label {
  font-weight: 600;
  color: #666;
  min-width: 100px;
}

.edit-btn {
  background: #007aff;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  cursor: pointer;
  width: fit-content;
}

.edit-btn:hover {
  background: #0056cc;
}

.empty-state {
  text-align: center;
  padding: 3rem;
  color: #666;
}

.browse-btn {
  background: #007aff;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 6px;
  cursor: pointer;
  margin-top: 1rem;
}

.properties-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
}

.property-card {
  border: 1px solid #eee;
  border-radius: 8px;
  overflow: hidden;
  transition: transform 0.2s;
}

.property-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.property-image {
  position: relative;
  height: 200px;
  background: #f5f5f5;
  display: flex;
  align-items: center;
  justify-content: center;
}

.property-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.property-status {
  position: absolute;
  top: 10px;
  right: 10px;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.8rem;
  font-weight: 600;
}

.property-status.booked {
  background: #ff9500;
  color: white;
}

.property-status.available {
  background: #34c759;
  color: white;
}

.property-info {
  padding: 1rem;
}

.property-info h3 {
  margin: 0 0 0.5rem 0;
  color: #2c3e50;
}

.property-address {
  color: #666;
  font-size: 0.9rem;
  margin-bottom: 0.5rem;
}

.property-price {
  font-size: 1.2rem;
  font-weight: 700;
  color: #007aff;
  margin-bottom: 1rem;
}

.property-actions {
  display: flex;
  gap: 0.5rem;
}

.action-btn {
  flex: 1;
  padding: 0.5rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
  transition: background-color 0.2s;
}

.action-btn.primary {
  background: #007aff;
  color: white;
}

.action-btn.primary:hover {
  background: #0056cc;
}

.action-btn.secondary {
  background: #f5f5f5;
  color: #666;
}

.action-btn.secondary:hover {
  background: #e5e5e5;
}

.search-filters {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin-bottom: 2rem;
  padding: 1.5rem;
  background: #f8f9fa;
  border-radius: 8px;
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.filter-group label {
  font-weight: 600;
  color: #2c3e50;
  font-size: 0.9rem;
}

.filter-group input,
.filter-group select {
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 1rem;
  transition: border-color 0.2s;
}

.filter-group input:focus,
.filter-group select:focus {
  outline: none;
  border-color: #007aff;
  box-shadow: 0 0 0 2px rgba(0, 122, 255, 0.1);
}

.search-btn,
.clear-btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 500;
  transition: background-color 0.2s;
  align-self: end;
}

.search-btn {
  background: #007aff;
  color: white;
}

.search-btn:hover {
  background: #0056cc;
}

.clear-btn {
  background: #6c757d;
  color: white;
}

.clear-btn:hover {
  background: #5a6268;
}

.search-results h3 {
  margin-bottom: 1rem;
  color: #2c3e50;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  min-width: 400px;
}

.modal-content h3 {
  margin-bottom: 1.5rem;
  color: #2c3e50;
}

.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 600;
  color: #666;
}

.form-group input {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.modal-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  margin-top: 2rem;
}

.btn-primary {
  background: #007aff;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
}

.btn-secondary {
  background: #f5f5f5;
  color: #666;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
}

/* Индикатор загрузки */
.loading-indicator {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem;
  text-align: center;
}

.loading-spinner {
  width: 50px;
  height: 50px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #007aff;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 1rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.loading-indicator p {
  color: #666;
  font-size: 1.1rem;
  margin: 0;
}

@media (max-width: 768px) {
  .dashboard-container {
    padding: 1rem;
  }
  
  .dashboard-header {
    flex-direction: column;
    gap: 1rem;
    align-items: stretch;
  }
  
  .header-actions {
    justify-content: center;
  }
  
  .properties-grid {
    grid-template-columns: 1fr;
  }
  
  .search-filters {
    grid-template-columns: 1fr;
  }
  
  .modal-content {
    margin: 1rem;
    min-width: auto;
  }
}
</style> 