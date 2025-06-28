import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'

createApp(App).mount('#app')

// Регистрация service worker для PWA
if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('/service-worker.js')
      .then(registration => {
        console.log('ServiceWorker зарегистрирован:', registration);
      })
      .catch(error => {
        console.log('Ошибка регистрации ServiceWorker:', error);
      });
  });
}
