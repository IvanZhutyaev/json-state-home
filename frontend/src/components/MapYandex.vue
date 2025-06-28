<template>
  <div class="map-container">
    <div id="map" style="width: 100%; height: 80vh; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.15);"></div>
    
    <div class="filters">
      <select id="classFilter" class="filter-select">
        <option value="">Все классы жилья</option>
      </select>

      <input 
        type="range" 
        min="0" 
        max="50000000" 
        step="1000000" 
        value="50000000"
        id="priceFilter" 
        class="filter-range" 
      />
      <label id="priceLabel">Максимальная цена: 50,000,000 ₽</label>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue';
import axios from 'axios';

onMounted(() => {
  let map = null;
  let allBuildings = [];
  let currentPlacemarks = [];

  // Данные по Краснодарскому краю и Адыгее
  allBuildings = [
    // Краснодар
    {
      id: 1,
      name: 'ЖК "Краснодарский"',
      address: 'ул. Красная, 139',
      latitude: 45.0448,
      longitude: 38.9760,
      price_from: 3000000,
      price_to: 8000000,
      housing_class: 'Комфорт'
    },
    {
      id: 2,
      name: 'ЖК "Эконом Краснодар"',
      address: 'ул. Северная, 45',
      latitude: 45.0522,
      longitude: 38.9725,
      price_from: 2000000,
      price_to: 5000000,
      housing_class: 'Эконом'
    },
    {
      id: 3,
      name: 'ЖК "Бизнес Краснодар"',
      address: 'ул. Гагарина, 25',
      latitude: 45.0488,
      longitude: 38.9780,
      price_from: 8000000,
      price_to: 20000000,
      housing_class: 'Бизнес'
    },
    // Сочи
    {
      id: 4,
      name: 'ЖК "Сочинский"',
      address: 'ул. Навагинская, 15',
      latitude: 43.6028,
      longitude: 39.7342,
      price_from: 5000000,
      price_to: 15000000,
      housing_class: 'Комфорт'
    },
    {
      id: 5,
      name: 'ЖК "Эконом Сочи"',
      address: 'ул. Горького, 30',
      latitude: 43.6088,
      longitude: 39.7302,
      price_from: 3000000,
      price_to: 8000000,
      housing_class: 'Эконом'
    },
    {
      id: 6,
      name: 'ЖК "Бизнес Сочи"',
      address: 'ул. Виноградная, 10',
      latitude: 43.6058,
      longitude: 39.7322,
      price_from: 12000000,
      price_to: 30000000,
      housing_class: 'Бизнес'
    },
    // Новороссийск
    {
      id: 7,
      name: 'ЖК "Новороссийский"',
      address: 'ул. Советов, 20',
      latitude: 44.7239,
      longitude: 37.7683,
      price_from: 2500000,
      price_to: 7000000,
      housing_class: 'Комфорт'
    },
    {
      id: 8,
      name: 'ЖК "Эконом Новороссийск"',
      address: 'ул. Ленина, 15',
      latitude: 44.7259,
      longitude: 37.7663,
      price_from: 1500000,
      price_to: 4000000,
      housing_class: 'Эконом'
    },
    // Армавир
    {
      id: 9,
      name: 'ЖК "Армавирский"',
      address: 'ул. Кирова, 25',
      latitude: 45.0013,
      longitude: 41.1194,
      price_from: 2000000,
      price_to: 6000000,
      housing_class: 'Комфорт'
    },
    {
      id: 10,
      name: 'ЖК "Эконом Армавир"',
      address: 'ул. Розы Люксембург, 10',
      latitude: 45.0033,
      longitude: 41.1174,
      price_from: 1200000,
      price_to: 3500000,
      housing_class: 'Эконом'
    },
    // Майкоп (Адыгея)
    {
      id: 11,
      name: 'ЖК "Майкопский"',
      address: 'ул. Краснооктябрьская, 15',
      latitude: 44.6068,
      longitude: 40.1052,
      price_from: 1800000,
      price_to: 5000000,
      housing_class: 'Комфорт'
    },
    {
      id: 12,
      name: 'ЖК "Эконом Майкоп"',
      address: 'ул. Пушкина, 20',
      latitude: 44.6088,
      longitude: 40.1032,
      price_from: 1000000,
      price_to: 3000000,
      housing_class: 'Эконом'
    },
    {
      id: 13,
      name: 'ЖК "Бизнес Майкоп"',
      address: 'ул. Гагарина, 8',
      latitude: 44.6048,
      longitude: 40.1072,
      price_from: 5000000,
      price_to: 12000000,
      housing_class: 'Бизнес'
    },
    // Анапа
    {
      id: 14,
      name: 'ЖК "Анапский"',
      address: 'ул. Крымская, 30',
      latitude: 44.8947,
      longitude: 37.3166,
      price_from: 3500000,
      price_to: 10000000,
      housing_class: 'Комфорт'
    },
    {
      id: 15,
      name: 'ЖК "Эконом Анапа"',
      address: 'ул. Ивана Голубца, 15',
      latitude: 44.8967,
      longitude: 37.3146,
      price_from: 2000000,
      price_to: 6000000,
      housing_class: 'Эконом'
    },
    // Геленджик
    {
      id: 16,
      name: 'ЖК "Геленджикский"',
      address: 'ул. Ленина, 25',
      latitude: 44.5608,
      longitude: 38.0765,
      price_from: 4000000,
      price_to: 12000000,
      housing_class: 'Комфорт'
    },
    {
      id: 17,
      name: 'ЖК "Бизнес Геленджик"',
      address: 'ул. Мира, 10',
      latitude: 44.5628,
      longitude: 38.0745,
      price_from: 10000000,
      price_to: 25000000,
      housing_class: 'Бизнес'
    }
  ];

  function createPlacemark(building) {
    let iconColor = 'blue';
    if (building.housing_class === 'Эконом') iconColor = 'red';
    else if (building.housing_class === 'Бизнес') iconColor = 'green';
    
    return new window.ymaps.Placemark([building.latitude, building.longitude], {
      balloonContentHeader: building.name,
      balloonContentBody: `
        <strong>Адрес:</strong> ${building.address}<br/>
        <strong>Цена:</strong> от ${building.price_from.toLocaleString()} ₽ до ${building.price_to.toLocaleString()} ₽<br/>
        <strong>Класс:</strong> ${building.housing_class}
      `
    }, {
      preset: `islands#${iconColor}HomeIcon`,
      iconColor: iconColor
    });
  }

  function updateMap() {
    if (!map) return;
    
    // Очищаем все метки
    map.geoObjects.removeAll();
    currentPlacemarks = [];
    
    const selectedClass = document.getElementById('classFilter').value;
    const maxPrice = parseInt(document.getElementById('priceFilter').value);
    
    // Фильтруем здания
    const filteredBuildings = allBuildings.filter(b => {
      const matchClass = selectedClass ? b.housing_class === selectedClass : true;
      const matchPrice = b.price_from <= maxPrice;
      return matchClass && matchPrice;
    });
    
    // Добавляем отфильтрованные метки
    filteredBuildings.forEach(building => {
      const placemark = createPlacemark(building);
      map.geoObjects.add(placemark);
      currentPlacemarks.push(placemark);
    });
  }

  function populateClassFilter() {
    const classFilter = document.getElementById('classFilter');
    const classes = [...new Set(allBuildings.map(b => b.housing_class))];
    
    classes.forEach(cls => {
      const option = document.createElement('option');
      option.value = cls;
      option.textContent = cls;
      classFilter.appendChild(option);
    });
  }

  function updatePriceLabel() {
    const priceFilter = document.getElementById('priceFilter');
    const priceLabel = document.getElementById('priceLabel');
    priceLabel.textContent = `Максимальная цена: ${parseInt(priceFilter.value).toLocaleString()} ₽`;
  }

  // Инициализация карты
  window.ymaps.ready(() => {
    map = new window.ymaps.Map('map', {
      center: [44.7239, 39.7342], // Центр между Краснодаром и Сочи
      zoom: 7, // Увеличиваем зум для лучшего обзора региона
      controls: ['zoomControl', 'fullscreenControl', 'geolocationControl', 'typeSelector']
    });

    // Заполняем фильтр классов
    populateClassFilter();
    
    // Добавляем обработчики событий
    document.getElementById('classFilter').addEventListener('change', updateMap);
    document.getElementById('priceFilter').addEventListener('input', () => {
      updatePriceLabel();
      updateMap();
    });

    // Добавляем все метки
    updateMap();
  });

  // Пробуем загрузить данные с API
  try {
    axios.get('http://localhost:8000/buildings')
      .then(response => {
        allBuildings = response.data;
        populateClassFilter();
        updateMap();
      })
      .catch(error => {
        console.error('Ошибка загрузки данных:', error);
        // Используем тестовые данные
      });
  } catch (error) {
    console.error('Ошибка загрузки данных:', error);
  }
});
</script>

<style scoped>
.map-container {
  width: 100vw;
  margin: 0;
  padding: 0;
  border-radius: 0;
}

#map {
  width: 100vw !important;
  height: 90vh !important;
  border-radius: 0 !important;
  margin: 0;
  box-shadow: none;
}

.filters {
  margin-top: 1rem;
  display: flex;
  gap: 1rem;
  align-items: center;
  flex-wrap: wrap;
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 8px;
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
}

.filter-select {
  padding: 0.5rem 1rem;
  font-size: 1rem;
  border-radius: 6px;
  border: 1px solid #ccc;
  min-width: 200px;
  background: white;
}

.filter-range {
  width: 200px;
}

label {
  white-space: nowrap;
  font-weight: 500;
  color: #333;
}
</style> 