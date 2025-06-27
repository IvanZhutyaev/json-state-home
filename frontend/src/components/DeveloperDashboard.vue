<template>
  <div class="dashboard-container">
    <div class="dashboard-header">
      <h1>Кабинет застройщика</h1>
      <div class="header-actions">
        <button class="back-btn" @click="goBack">← Вернуться</button>
        <button class="logout-btn" @click="logout">Выйти</button>
      </div>
    </div>

    <div class="dashboard-content">
      <!-- Аналитика -->
      <div class="dashboard-section">
        <h2>Аналитика</h2>
        <div class="analytics-grid">
          <div class="analytics-card">
            <div class="analytics-icon">📊</div>
            <div class="analytics-content">
              <h3>Всего ЖК</h3>
              <p class="analytics-number">{{ analytics.totalComplexes }}</p>
            </div>
          </div>
          <div class="analytics-card">
            <div class="analytics-icon">🏠</div>
            <div class="analytics-content">
              <h3>Всего квартир</h3>
              <p class="analytics-number">{{ analytics.totalApartments }}</p>
            </div>
          </div>
          <div class="analytics-card">
            <div class="analytics-icon">💰</div>
            <div class="analytics-content">
              <h3>Продано</h3>
              <p class="analytics-number">{{ analytics.soldApartments }}</p>
            </div>
          </div>
          <div class="analytics-card">
            <div class="analytics-icon">📈</div>
            <div class="analytics-content">
              <h3>Доход</h3>
              <p class="analytics-number">{{ analytics.totalRevenue }} ₽</p>
            </div>
          </div>
        </div>
      </div>

      <!-- ЖК застройщика -->
      <div class="dashboard-section">
        <div class="section-header">
          <h2>Жилые комплексы</h2>
          <button class="add-btn" @click="showAddComplexModal = true">
            + Добавить ЖК
          </button>
        </div>
        
        <div class="complexes-grid">
          <div 
            v-for="complex in complexes" 
            :key="complex.id"
            class="complex-card"
          >
            <div class="complex-image">
              <img :src="complex.image" :alt="complex.name" />
              <div class="complex-status" :class="complex.status">
                {{ complex.statusText }}
              </div>
            </div>
            <div class="complex-info">
              <h3>{{ complex.name }}</h3>
              <p class="complex-address">{{ complex.address }}</p>
              <div class="complex-stats">
                <span>Квартир: {{ complex.apartmentsCount }}</span>
                <span>Продано: {{ complex.soldCount }}</span>
              </div>
              <div class="complex-actions">
                <button class="action-btn primary" @click="viewComplex(complex.id)">
                  Просмотр
                </button>
                <button class="action-btn secondary" @click="editComplex(complex.id)">
                  Редактировать
                </button>
                <button class="action-btn secondary" @click="addApartment(complex.id)">
                  + Квартира
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Забронированные квартиры -->
      <div class="dashboard-section">
        <h2>Забронированные квартиры</h2>
        <div v-if="bookedApartments.length === 0" class="empty-state">
          <p>Нет забронированных квартир</p>
        </div>
        <div v-else class="apartments-grid">
          <div 
            v-for="apartment in bookedApartments" 
            :key="apartment.id"
            class="apartment-card"
          >
            <div class="apartment-image">
              <img :src="apartment.image" :alt="apartment.name" />
              <div class="apartment-status booked">Забронировано</div>
            </div>
            <div class="apartment-info">
              <h3>{{ apartment.name }}</h3>
              <p class="apartment-address">{{ apartment.address }}</p>
              <p class="apartment-price">{{ apartment.price }} ₽</p>
              <p class="apartment-client">Клиент: {{ apartment.clientName }}</p>
              <div class="apartment-actions">
                <button class="action-btn primary" @click="confirmSale(apartment.id)">
                  Подтвердить продажу
                </button>
                <button class="action-btn secondary" @click="cancelBooking(apartment.id)">
                  Отменить бронь
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Проданные объекты -->
      <div class="dashboard-section">
        <h2>Проданные объекты</h2>
        <div v-if="soldApartments.length === 0" class="empty-state">
          <p>Нет проданных объектов</p>
        </div>
        <div v-else class="apartments-grid">
          <div 
            v-for="apartment in soldApartments" 
            :key="apartment.id"
            class="apartment-card"
          >
            <div class="apartment-image">
              <img :src="apartment.image" :alt="apartment.name" />
              <div class="apartment-status sold">Продано</div>
            </div>
            <div class="apartment-info">
              <h3>{{ apartment.name }}</h3>
              <p class="apartment-address">{{ apartment.address }}</p>
              <p class="apartment-price">{{ apartment.price }} ₽</p>
              <p class="apartment-client">Покупатель: {{ apartment.buyerName }}</p>
              <p class="apartment-date">Дата продажи: {{ apartment.saleDate }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Личная информация застройщика -->
      <div class="dashboard-section">
        <h2>Личная информация</h2>
        <div class="developer-info">
          <div class="info-item">
            <label>Название компании:</label>
            <span>{{ developerInfo.companyName }}</span>
          </div>
          <div class="info-item">
            <label>ИНН:</label>
            <span>{{ developerInfo.inn }}</span>
          </div>
          <div class="info-item">
            <label>ОГРН:</label>
            <span>{{ developerInfo.ogrn }}</span>
          </div>
          <div class="info-item">
            <label>Адрес:</label>
            <span>{{ developerInfo.address }}</span>
          </div>
          <div class="info-item">
            <label>Представитель:</label>
            <span>{{ developerInfo.representative }}</span>
          </div>
          <button class="edit-btn" @click="editDeveloperProfile">Редактировать</button>
        </div>
      </div>
    </div>

    <!-- Модальное окно добавления ЖК -->
    <div v-if="showAddComplexModal" class="modal-overlay" @click="closeAddComplexModal">
      <div class="modal-content" @click.stop>
        <h3>Добавить новый ЖК</h3>
        <div class="form-group">
          <label>Название ЖК:</label>
          <input v-model="newComplex.name" type="text" placeholder="Введите название" />
        </div>
        <div class="form-group">
          <label>Адрес:</label>
          <input v-model="newComplex.address" type="text" placeholder="Введите адрес" />
        </div>
        <div class="form-group">
          <label>Город:</label>
          <select v-model="newComplex.city">
            <option value="">Выберите город</option>
            <option value="Краснодар">Краснодар</option>
            <option value="Адыгея">Адыгея</option>
          </select>
        </div>
        <div class="form-group">
          <label>Год ввода в эксплуатацию:</label>
          <select v-model="newComplex.year">
            <option value="">Выберите год</option>
            <option value="2025">2025</option>
            <option value="2030">2030</option>
          </select>
        </div>
        <div class="form-group">
          <label>Класс ЖК:</label>
          <select v-model="newComplex.building_type">
            <option value="">Выберите класс</option>
            <option value="Эконом">Эконом</option>
            <option value="Комфорт">Комфорт</option>
            <option value="Бизнес">Бизнес</option>
          </select>
        </div>
        <div class="form-group">
          <label>Статус:</label>
          <select v-model="newComplex.status">
            <option value="">Выберите статус</option>
            <option value="Готов">Готов</option>
            <option value="Строится">Строится</option>
          </select>
        </div>
        <div class="modal-actions">
          <button class="btn-secondary" @click="closeAddComplexModal">Отмена</button>
          <button class="btn-primary" @click="addComplex">Добавить ЖК</button>
        </div>
      </div>
    </div>

    <!-- Модальное окно добавления квартиры -->
    <div v-if="showAddApartmentModal" class="modal-overlay" @click="closeAddApartmentModal">
      <div class="modal-content" @click.stop>
        <h3>Добавить квартиру</h3>
        <div class="form-group">
          <label>Номер квартиры:</label>
          <input v-model="newApartment.number" type="text" placeholder="Например: 45" />
        </div>
        <div class="form-group">
          <label>Площадь (м²):</label>
          <input v-model="newApartment.area" type="number" placeholder="75.5" />
        </div>
        <div class="form-group">
          <label>Количество комнат:</label>
          <select v-model="newApartment.rooms">
            <option value="1">1</option>
            <option value="2">2</option>
            <option value="3">3</option>
            <option value="4">4+</option>
          </select>
        </div>
        <div class="form-group">
          <label>Этаж:</label>
          <input v-model="newApartment.floor" type="number" placeholder="5" />
        </div>
        <div class="form-group">
          <label>Цена (₽):</label>
          <input v-model="newApartment.price" type="number" placeholder="3200000" />
        </div>
        <div class="form-group">
          <label>Изображение:</label>
          <input v-model="newApartment.image" type="url" placeholder="URL изображения" />
        </div>
        <div class="modal-actions">
          <button class="btn-secondary" @click="closeAddApartmentModal">Отмена</button>
          <button class="btn-primary" @click="addApartmentToComplex">Добавить квартиру</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'

const emit = defineEmits(['logout', 'go-back'])

// Аналитика
const analytics = ref({
  totalComplexes: 3,
  totalApartments: 156,
  soldApartments: 89,
  totalRevenue: '284,500,000'
})

// ЖК застройщика
const complexes = ref([
  {
    id: 1,
    name: 'ЖК "Солнечный"',
    address: 'г. Москва, ул. Солнечная, 15',
    status: 'active',
    statusText: 'Активен',
    apartmentsCount: 45,
    soldCount: 32,
    image: 'https://via.placeholder.com/300x200/007aff/ffffff?text=ЖК+Солнечный'
  },
  {
    id: 2,
    name: 'ЖК "Парковый"',
    address: 'г. Москва, ул. Парковая, 8',
    status: 'active',
    statusText: 'Активен',
    apartmentsCount: 78,
    soldCount: 45,
    image: 'https://via.placeholder.com/300x200/34c759/ffffff?text=ЖК+Парковый'
  },
  {
    id: 3,
    name: 'ЖК "Речной"',
    address: 'г. Москва, наб. Речная, 12',
    status: 'construction',
    statusText: 'Строительство',
    apartmentsCount: 33,
    soldCount: 12,
    image: 'https://via.placeholder.com/300x200/ff9500/ffffff?text=ЖК+Речной'
  }
])

// Забронированные квартиры
const bookedApartments = ref([
  {
    id: 1,
    name: 'ЖК "Солнечный", кв. 45',
    address: 'г. Москва, ул. Солнечная, 15',
    price: '3,200,000',
    clientName: 'Иван Петров',
    image: 'https://via.placeholder.com/300x200/007aff/ffffff?text=Кв.+45'
  }
])

// Проданные объекты
const soldApartments = ref([
  {
    id: 2,
    name: 'ЖК "Парковый", кв. 78',
    address: 'г. Москва, ул. Парковая, 8',
    price: '4,100,000',
    buyerName: 'Анна Сидорова',
    saleDate: '15.03.2024',
    image: 'https://via.placeholder.com/300x200/34c759/ffffff?text=Кв.+78'
  }
])

// Личная информация застройщика
const developerInfo = ref({
  companyName: 'ООО "СтройИнвест"',
  inn: '1234567890',
  ogrn: '1234567890123',
  address: 'г. Москва, ул. Строительная, 1',
  representative: 'Петров И.И., директор'
})

// Модальные окна
const showAddComplexModal = ref(false)
const showAddApartmentModal = ref(false)

// Формы
const newComplex = reactive({
  name: '',
  address: '',
  city: '',
  year: '',
  building_type: '',
  status: ''
})

const newApartment = reactive({
  number: '',
  area: '',
  rooms: '1',
  floor: '',
  price: '',
  image: ''
})

// Методы
const logout = () => {
  // Эмитим событие для родительского компонента
  emit('logout')
}

const goBack = () => {
  // Эмитим событие для возврата на главную страницу
  emit('go-back')
}

const viewComplex = (complexId) => {
  console.log('Просмотр ЖК:', complexId)
}

const editComplex = (complexId) => {
  console.log('Редактирование ЖК:', complexId)
}

const addApartment = (complexId) => {
  showAddApartmentModal.value = true
}

const confirmSale = (apartmentId) => {
  console.log('Подтверждение продажи:', apartmentId)
}

const cancelBooking = (apartmentId) => {
  console.log('Отмена брони:', apartmentId)
}

const editDeveloperProfile = () => {
  console.log('Редактирование профиля застройщика')
}

const closeAddComplexModal = () => {
  showAddComplexModal.value = false
  Object.keys(newComplex).forEach(key => newComplex[key] = '')
}

const closeAddApartmentModal = () => {
  showAddApartmentModal.value = false
  Object.keys(newApartment).forEach(key => newApartment[key] = '')
}

const addComplex = async () => {
  // Проверяем, что все обязательные поля заполнены
  if (!newComplex.name || !newComplex.address || !newComplex.city || 
      !newComplex.year || !newComplex.building_type || !newComplex.status) {
    alert('Пожалуйста, заполните все обязательные поля')
    return
  }

  // Формируем JSON в нужном формате
  const complexData = {
    name: newComplex.name,
    address: newComplex.address,
    city: newComplex.city,
    year: parseInt(newComplex.year),
    building_type: newComplex.building_type,
    status: newComplex.status,
    developer_id: 1
  }

  try {
    const response = await fetch('http://localhost:8000/properties/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(complexData)
    })

    if (response.ok) {
      const result = await response.json()
      console.log('ЖК успешно создан:', result)
      alert('ЖК успешно добавлен!')
      closeAddComplexModal()
      // Здесь можно добавить обновление списка ЖК
    } else {
      const errorData = await response.json()
      alert(`Ошибка создания ЖК: ${errorData.detail}`)
    }
  } catch (error) {
    console.error('Ошибка при создании ЖК:', error)
    alert('Ошибка сети при создании ЖК')
  }
}

const addApartmentToComplex = () => {
  console.log('Добавление квартиры:', newApartment)
  closeAddApartmentModal()
}

onMounted(() => {
  console.log('Загрузка данных застройщика')
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
}

.back-btn {
  background: #f5f5f5;
  color: #666;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 500;
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

.dashboard-content {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  margin-bottom: 2rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
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

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.section-header h2 {
  margin: 0;
}

.add-btn {
  background: #34c759;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 500;
}

.add-btn:hover {
  background: #28a745;
}

/* Аналитика */
.analytics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
}

.analytics-card {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1.5rem;
  background: linear-gradient(135deg, #007aff, #0056cc);
  color: white;
  border-radius: 8px;
}

.analytics-icon {
  font-size: 2rem;
  width: 50px;
  text-align: center;
}

.analytics-content h3 {
  margin: 0 0 0.5rem 0;
  font-size: 1rem;
  opacity: 0.9;
}

.analytics-number {
  margin: 0;
  font-size: 1.5rem;
  font-weight: 700;
}

/* ЖК */
.complexes-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 1.5rem;
}

.complex-card {
  border: 1px solid #eee;
  border-radius: 8px;
  overflow: hidden;
  transition: transform 0.2s;
}

.complex-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.complex-image {
  position: relative;
  height: 200px;
  background: #f5f5f5;
}

.complex-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.complex-status {
  position: absolute;
  top: 10px;
  right: 10px;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.8rem;
  font-weight: 600;
}

.complex-status.active {
  background: #34c759;
  color: white;
}

.complex-status.construction {
  background: #ff9500;
  color: white;
}

.complex-info {
  padding: 1rem;
}

.complex-info h3 {
  margin: 0 0 0.5rem 0;
  color: #2c3e50;
}

.complex-address {
  color: #666;
  font-size: 0.9rem;
  margin-bottom: 1rem;
}

.complex-stats {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
  font-size: 0.9rem;
  color: #666;
}

.complex-actions {
  display: flex;
  gap: 0.5rem;
}

/* Квартиры */
.apartments-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
}

.apartment-card {
  border: 1px solid #eee;
  border-radius: 8px;
  overflow: hidden;
  transition: transform 0.2s;
}

.apartment-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.apartment-image {
  position: relative;
  height: 200px;
  background: #f5f5f5;
}

.apartment-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.apartment-status {
  position: absolute;
  top: 10px;
  right: 10px;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.8rem;
  font-weight: 600;
}

.apartment-status.booked {
  background: #ff9500;
  color: white;
}

.apartment-status.sold {
  background: #34c759;
  color: white;
}

.apartment-info {
  padding: 1rem;
}

.apartment-info h3 {
  margin: 0 0 0.5rem 0;
  color: #2c3e50;
}

.apartment-address {
  color: #666;
  font-size: 0.9rem;
  margin-bottom: 0.5rem;
}

.apartment-price {
  font-size: 1.2rem;
  font-weight: 700;
  color: #007aff;
  margin-bottom: 0.5rem;
}

.apartment-client,
.apartment-date {
  color: #666;
  font-size: 0.9rem;
  margin-bottom: 0.5rem;
}

.apartment-actions {
  display: flex;
  gap: 0.5rem;
  margin-top: 1rem;
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

/* Личная информация */
.developer-info {
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
  min-width: 150px;
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

/* Модальные окна */
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
  z-index: 2000;
  padding: 1rem;
}

.modal-content {
  background: white;
  border-radius: 12px;
  max-width: 500px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
  padding: 2rem;
}

.modal-content h3 {
  margin: 0 0 1.5rem 0;
  color: #2c3e50;
  font-size: 1.5rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  color: #2c3e50;
  font-weight: 500;
}

.form-group input,
.form-group textarea,
.form-group select {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 1rem;
  transition: border-color 0.2s;
}

.form-group input:focus,
.form-group textarea:focus,
.form-group select:focus {
  outline: none;
  border-color: #007aff;
  box-shadow: 0 0 0 2px rgba(0, 122, 255, 0.1);
}

.form-group select {
  background: white;
  cursor: pointer;
}

.form-group select option {
  padding: 0.5rem;
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
  padding: 0.75rem 1.5rem;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 500;
  transition: background-color 0.2s;
}

.btn-primary:hover {
  background: #0056cc;
}

.btn-secondary {
  background: #f5f5f5;
  color: #666;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 500;
  transition: background-color 0.2s;
}

.btn-secondary:hover {
  background: #e5e5e5;
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
  
  .analytics-grid {
    grid-template-columns: 1fr;
  }
  
  .complexes-grid,
  .apartments-grid {
    grid-template-columns: 1fr;
  }
  
  .section-header {
    flex-direction: column;
    gap: 1rem;
    align-items: stretch;
  }
  
  .modal-content {
    margin: 1rem;
    min-width: auto;
  }
}
</style> 