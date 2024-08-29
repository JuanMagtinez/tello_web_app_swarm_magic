import { createApp } from 'vue'
import App from './App.vue'
import router from './router';

import { IonicVue } from '@ionic/vue';

/* Core CSS required for Ionic components to work properly */
import '@ionic/vue/css/core.css';

/* Basic CSS for apps built with Ionic */
import '@ionic/vue/css/normalize.css';
import '@ionic/vue/css/structure.css';
import '@ionic/vue/css/typography.css';

/* Optional CSS utils that can be commented out */
import '@ionic/vue/css/padding.css';
import '@ionic/vue/css/float-elements.css';
import '@ionic/vue/css/text-alignment.css';
import '@ionic/vue/css/text-transformation.css';
import '@ionic/vue/css/flex-utils.css';
import '@ionic/vue/css/display.css';

/* Theme variables */
import './theme/variables.css';

import mqttVueHook from 'mqtt-vue-hook';

const app = createApp(App)
app.use(IonicVue)
app.use(router);

// ws://broker.hivemq.com:8000/mqtt
app.use(mqttVueHook, 'ws://broker.hivemq.com:8000/mqtt', {
  clean: false,
  keepalive: 60,
  clientId: 'MyAppTelloDrone',
  connectTimeout: 4000,
})
  
router.isReady().then(() => {
  app.mount('#app');
});