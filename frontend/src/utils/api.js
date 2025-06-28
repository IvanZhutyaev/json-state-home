const API_BASE_URL = 'http://localhost:8000'

// Функция для выполнения HTTP запросов
async function apiRequest(endpoint, options = {}) {
  const url = `${API_BASE_URL}${endpoint}`
  const config = {
    headers: {
      'Content-Type': 'application/json',
      ...options.headers
    },
    ...options
  }

  try {
    const response = await fetch(url, config)
    
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}))
      throw new Error(errorData.detail || `HTTP error! status: ${response.status}`)
    }
    
    return await response.json()
  } catch (error) {
    console.error('API request failed:', error)
    throw error
  }
}

// API для пользователей
export const userAPI = {
  // Регистрация пользователя
  register: (userData) => 
    apiRequest('/users/', {
      method: 'POST',
      body: JSON.stringify(userData)
    }),
  
  // Получить пользователя по ID
  getUser: (userId) => apiRequest(`/users/${userId}`),
  
  // Обновить профиль пользователя
  updateProfile: (userId, name, phone) => 
    apiRequest(`/users/${userId}/profile?name=${encodeURIComponent(name)}&phone=${encodeURIComponent(phone)}`, {
      method: 'PUT'
    }),
  
  // Вход пользователя
  login: (credentials) => 
    apiRequest('/users/login', {
      method: 'POST',
      body: JSON.stringify(credentials)
    })
}

// API для застройщиков
export const developerAPI = {
  // Регистрация застройщика
  register: (zastroyData) => 
    apiRequest('/zastroys/', {
      method: 'POST',
      body: JSON.stringify(zastroyData)
    }),
  
  // Вход застройщика
  login: (credentials) => 
    apiRequest('/zastroys/login', {
      method: 'POST',
      body: JSON.stringify(credentials)
    }),
  
  // Получить застройщика по ID
  getDeveloper: (developerId) => apiRequest(`/zastroys/${developerId}`),
  
  // Получить все ЖК застройщика (из таблицы Properties)
  getDeveloperProperties: (developerId) => apiRequest(`/properties/?zastroy_id=${developerId}`),
  
  // Получить все жилые комплексы застройщика (из таблицы ResidentialComplex)
  getDeveloperResidentialComplexes: (developerName) => 
    apiRequest(`/zastroys/residential-complexes/?developer_name=${encodeURIComponent(developerName)}`),
  
  // Создать новый ЖК
  createProperty: (propertyData) => 
    apiRequest('/properties/', {
      method: 'POST',
      body: JSON.stringify(propertyData)
    }),
  
  // Создать новый жилой комплекс
  createResidentialComplex: (complexData) => 
    apiRequest('/zastroys/residential-complexes/', {
      method: 'POST',
      body: JSON.stringify(complexData)
    }),
  
  // Создать новую квартиру в ЖК
  createApartment: (apartmentData) => 
    apiRequest('/properties/', {
      method: 'POST',
      body: JSON.stringify(apartmentData)
    }),
  
  // Получить квартиры конкретного ЖК
  getComplexApartments: (complexId) => 
    apiRequest(`/properties/?complex_id=${complexId}`),
  
  // Обновить ЖК
  updateProperty: (propertyId, propertyData) => 
    apiRequest(`/properties/${propertyId}`, {
      method: 'PUT',
      body: JSON.stringify(propertyData)
    }),
  
  // Удалить ЖК
  deleteProperty: (propertyId) => 
    apiRequest(`/properties/${propertyId}`, {
      method: 'DELETE'
    })
}

// API для недвижимости
export const propertyAPI = {
  // Получить все объекты недвижимости
  getAllProperties: () => apiRequest('/properties/'),
  
  // Поиск недвижимости
  searchProperties: (params) => {
    const searchParams = new URLSearchParams()
    if (params.city) searchParams.append('city', params.city)
    if (params.minPrice) searchParams.append('min_price', params.minPrice)
    if (params.maxPrice) searchParams.append('max_price', params.maxPrice)
    if (params.rooms) searchParams.append('rooms', params.rooms)
    if (params.minArea) searchParams.append('min_area', params.minArea)
    if (params.maxArea) searchParams.append('max_area', params.maxArea)
    if (params.isAvailable !== undefined) searchParams.append('is_available', params.isAvailable)
    
    return apiRequest(`/properties/search?${searchParams.toString()}`)
  },
  
  // Получить конкретный объект недвижимости
  getProperty: (propertyId) => apiRequest(`/properties/${propertyId}`),
  
  // Забронировать недвижимость
  bookProperty: (propertyId, userId) => 
    apiRequest(`/properties/book?user_id=${userId}`, {
      method: 'POST',
      body: JSON.stringify({ property_id: propertyId }),
      headers: {
        'Content-Type': 'application/json'
      }
    }),
  
  // Получить брони пользователя
  getUserBookings: (userId) => apiRequest(`/properties/bookings/${userId}`),
  
  // Отменить бронь
  cancelBooking: (bookingId, userId) => 
    apiRequest(`/properties/bookings/${bookingId}/cancel?user_id=${userId}`, {
      method: 'POST'
    }),
  
  // Купить недвижимость
  purchaseProperty: (bookingId, userId) => 
    apiRequest(`/properties/bookings/${bookingId}/purchase?user_id=${userId}`, {
      method: 'POST'
    })
}

export default {
  userAPI,
  propertyAPI,
  developerAPI
} 