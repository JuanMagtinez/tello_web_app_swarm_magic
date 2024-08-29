<template>
    <ion-page>
      <ion-header>
        <ion-toolbar>

            <ion-buttons slot="primary">
            <ion-button href="/">
                <ion-icon slot="icon-only" :icon="exit"></ion-icon>
            </ion-button>
            </ion-buttons>

            <ion-buttons slot="start">
            <ion-menu-button :auto-hide="false"></ion-menu-button>
            </ion-buttons>

            <ion-title class="ion-text-center" text-align: center>Waiting room</ion-title>

        </ion-toolbar>
      </ion-header>
      <ion-progress-bar :buffer="buffer" :value="progress">
        <ion-router>
          <ion-route-redirect from="/DroneWaitingPage" to="/Simple/DroneControllPage"></ion-route-redirect>
          
      </ion-router>
      </ion-progress-bar>
      <ion-content>
        
      </ion-content>
    </ion-page>
</template>
  
<script>
  import { defineComponent, ref, onMounted } from 'vue';
  import { IonHeader, IonToolbar, IonContent, IonButton, IonIcon, IonMenuButton, IonProgressBar } from '@ionic/vue';
  import { exit } from 'ionicons/icons';
  import { useRouter } from 'vue-router';
  import { useMQTT } from 'mqtt-vue-hook';
  
  export default  defineComponent({
    name: 'ComponentTab',
    components: { IonHeader, IonToolbar, IonContent, IonButton, IonIcon, IonMenuButton, IonProgressBar }, 

    setup() {
        const buffer = ref(0.06)
        const progress = ref(0)
            
        const interval = setInterval(() => {
            console.log('waiting...');
            buffer.value += 0.06;
            progress.value += 0.06;
        }, 1000);

        // onMounted (()=>{

        // })
      
        return {
            interval,
            buffer,
            progress,
            exit
        }
    }
  })
</script>

<style>



</style>
  