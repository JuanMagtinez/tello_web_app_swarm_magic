<template>
    <ion-page>
      <ion-header>
        <ion-toolbar>
          <ion-title class="ion-text-center">Drone Engineering Ecosystem</ion-title>
          <ion-progress-bar v-if = "connecting" type="indeterminate"></ion-progress-bar>
        </ion-toolbar>
      </ion-header>
      <ion-content>
        <div style="margin-top: 20px;">
         
        </div>
        <div style="display: flex; justify-content: center">
          <ion-button :disabled="connecting" @click = 'connect' class="connectButton" >Connect to the tello drone</ion-button>
        </div>
        <div style="display: flex; justify-content: center">
          <ion-button :disabled="connecting" @click = "connectSwarm" class="connectButton" >Connect to the swarm</ion-button>
        </div>
        
      </ion-content>
    </ion-page>
</template>
  
<script>
  import { defineComponent, ref, onMounted } from 'vue';
  import { IonPage, IonHeader, IonToolbar, IonTitle, IonContent, IonButton,   IonProgressBar } from '@ionic/vue';
  import { useRouter } from 'vue-router';
  import { useMQTT } from 'mqtt-vue-hook'
 
  
  export default  defineComponent({
    name: 'ComponentTab',
    components: { IonHeader, IonToolbar, IonTitle, IonContent, IonPage, IonButton, IonProgressBar }, 

    setup() {
      const nameInput = ref(undefined);
      const ageInput = ref(undefined);
      const router = useRouter();
      const mqttHook = useMQTT()
      const User = ref();
      const connecting = ref(false)
      
      

      function connect () {
       
          
          mqttHook.publish('Connect','myAppTello',1)
          mqttHook.publish('command')
        
        
      }
      function connectSwarm () {
        mqttHook.publish('ConnectSwarm','myAppTello',1)
      }

     

      

      onMounted (()=>{
        mqttHook.subscribe('connected', 1)
        mqttHook.registerEvent('connected', (topic, message) => {
          router.push('/Simple/DroneControllPage')
          console.log(topic)
          User.value = JSON.parse(message)
          if (User.value == 2){
            console.log('PLAYER 1')
            connecting.value = true
          }
          /*else if (User.value == 2){
            console.log('PLAYER 2')
            router.push('/DroneWaitingPage')
          }*/
          else{
            Alert_full()
          }
        });
        mqttHook.subscribe('StartGame', 1)
        mqttHook.registerEvent('StartGame', () => {
          
          router.push('/Simple/DroneControllPage')
        })
        mqttHook.subscribe('connectedSwarm', 1)
        mqttHook.registerEvent('connectedSwarm', () => {
          router.push('/Swarm')
        })
      })
      
      return {
        connect,
        connectSwarm,
        
        router,
        
        onMounted,
        User,
        connecting
        
      }
    }
  })
</script>

<style>

.connectButton {
  display: flex;
  margin-top: 30px;
  width: 300px;
  height:300px;
  background: red;
}
.row-container {
  display: flex;
  justify-content: space-between; /* Alinea los botones horizontalmente */
}

</style>
  