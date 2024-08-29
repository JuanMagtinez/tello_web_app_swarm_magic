<template>
    <ion-page>
      <ion-header>
        <ion-toolbar>
          <ion-buttons slot="primary">
            <ion-button href="/">
              <ion-icon slot="icon-only" :icon="exit"></ion-icon>
            </ion-button>
          </ion-buttons>
          
          <ion-title class="ion-text-center">Swarm</ion-title>
        </ion-toolbar>
      </ion-header> 
      <ion-content :fullscreen="true">
    <div style="display: flex;">
        <div style="margin: 20px">
        <label style="margin-right: 10px;">Drone_1 battery:</label>
        <ion-icon v-if = "battery1<20" :icon="batteryDead" color="red"/>
        <ion-icon v-if = "battery1<=70 && battery1>=20" :icon="batteryHalf"/>
        <ion-icon v-if = "battery1>70" :icon="batteryFull"/>
        <label style="margin-left: 10px;">{{ battery1 }} %</label>
      </div>
      <div style="margin: 20px">
        <label style="margin-right: 10px;">Drone_2 battery:</label>
        <ion-icon v-if = "battery2<20" :icon="batteryDead" color="red"/>
        <ion-icon v-if = "battery2<=70 && battery2>=20" :icon="batteryHalf"/>
        <ion-icon v-if = "battery2>70" :icon="batteryFull"/>
        <label style="margin-left: 10px;">{{ battery2 }} %</label>
      </div>
      
        <div style="margin: 20px">
        <label style="margin-right: 10px;">Drone_3 battery:</label>
        <ion-icon v-if = "battery3<20" :icon="batteryDead" color="red"/>
        <ion-icon v-if = "battery3<=70 && battery3>=20" :icon="batteryHalf"/>
        <ion-icon v-if = "battery3>70" :icon="batteryFull"/>
        <label style="margin-left: 10px;">{{ battery3 }} %</label>
      </div>
      <div style="margin: 20px">
        <label style="margin-right: 10px;">Drone_4 battery:</label>
        <ion-icon v-if = "battery4<20" :icon="batteryDead" color="red"/>
        <ion-icon v-if = "battery4<=70 && battery4>=20" :icon="batteryHalf"/>
        <ion-icon v-if = "battery4>70" :icon="batteryFull"/>
        <label style="margin-left: 10px;">{{ battery4 }} %</label>
      </div>
    </div>
        <div style="margin: 50px" class="autopilot">
          <ion-button class="autopilotButton" @click="takeOff">Take Off</ion-button>
          <ion-button class="autopilotButton" @click="land">Land</ion-button>
          <ion-button class="autopilotButton" @click="Flip">Flip</ion-button>
          <ion-button class="autopilotButton" @click="BasicLines">WAVING</ion-button>
          <ion-button class="autopilotButton" @click="estabilidad">SHOW</ion-button>

        </div>

        <div style="margin: 20px"></div>

        <div style="margin-top: 40px;">
        <div class="direction">

            <div class="buttonTurnL"></div>

            <div class="buttonForward">
                <ion-icon :icon="arrowUp" size="large" id="forward" v-on:click="go($event)"/>
            </div>

            <div class="buttonTurnR"></div>

        </div>
        <div class="direction">  
          
            <div class="buttonLeft">
                <ion-icon :icon="arrowBack" size="large" id="left" v-on:click="go($event)"/>
            </div>

            <div class="buttonStop"></div>

            <div class="buttonRight">
                <ion-icon :icon="arrowForward" size="large" id="right" v-on:click="go($event)"/>
            </div>

        </div>
        <!-- <div class="direction">

            <div class="buttonUp"></div>

            <div class="buttonBack">
                <ion-icon :icon="arrowDown" size="large" id="back" v-on:click="go($event)"/>
            </div>

            <div class="buttonDown"></div>

        </div> -->
      </div>
  
      </ion-content>
    </ion-page>
  </template>
  
  <script>
  import { IonPage, IonHeader, IonToolbar, IonTitle, IonContent, IonButton, IonButtons, IonIcon } from '@ionic/vue';
  import { exit, arrowUp, arrowBack, arrowForward, arrowDown, batteryDead, batteryHalf, batteryFull} from 'ionicons/icons';
  import { defineComponent, ref, onMounted } from 'vue'
  import { useMQTT } from 'mqtt-vue-hook'
  
  export default  defineComponent({
    name: 'CameraPage',
    components: { IonHeader, IonToolbar, IonTitle, IonContent, IonPage, IonButton, IonButtons, IonIcon },
  
    setup () {
      const mqttHook = useMQTT()
      const battery1 = ref(0);
      const battery2 = ref(0);
      const battery3 = ref(0);
      const battery4 = ref(0);

      function takeOff(){
      mqttHook.publish('takeoff','',1)
      mqttHook.publish('stop','',1)
      }

      function land(){
        mqttHook.publish('land','',1)
      }
       function Flip(){
        mqttHook.publish('Flip','',1)
      }
      
       function BasicLines(){
        mqttHook.publish('BasicLines','',1)
      }

      function estabilidad(){
        mqttHook.publish('estabilidad','',1)
      }

      function go (event) {
        const dir = event.currentTarget.id;
        mqttHook.publish(dir,'0',1)  
        console.log(dir)   
      }
      onMounted (()=>{
      mqttHook.subscribe('battery1', 1);
      mqttHook.registerEvent('battery1', (topic, message) => {
        battery1.value = message;
      })
      mqttHook.subscribe('battery2', 1);
      mqttHook.registerEvent('battery2', (topic, message) => {
        battery2.value = message;
      })
      mqttHook.subscribe('battery3', 1);
      mqttHook.registerEvent('battery3', (topic, message) => {
        battery3.value = message;
      })
      mqttHook.subscribe('battery4', 1);
      mqttHook.registerEvent('battery4', (topic, message) => {
        battery4.value = message;
      })
      });
      
      return {
        arrowUp, 
        arrowBack, 
        arrowForward, 
        arrowDown,
        exit,
        takeOff,
        land,
        Flip,
        BasicLines,
        estabilidad,
        go,
        batteryDead,
        batteryHalf,
        batteryFull,
        battery1,
        battery2,
        battery3,
        battery4

      }
    }
  });
  </script>
  
  <style>
    .buttonTurnL {
    width: 100px;
    height: 100px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: rgb(16, 26, 205);
    font-size: 18px;
  }
  .buttonForward {
    width: 100px;
    height: 100px;
    border-top: 2px solid  rgb(16, 26, 205);
    border-left: 2px solid  rgb(16, 26, 205);
    border-right: 2px solid  rgb(16, 26, 205);
    display: flex;
    align-items: center;
    justify-content: center;
    color: rgb(16, 26, 205);
    font-size: 18px;
  }
  .buttonTurnR {
    width: 100px;
    height: 100px;
    display: flex;
    align-items: center;
    justify-content: center;
    color:  rgb(16, 26, 205);
    font-size: 18px;
  }
  .buttonLeft {
    width: 100px;
    height: 100px;
    border-top: 2px solid  rgb(16, 26, 205);
    border-left: 2px solid  rgb(16, 26, 205);
    border-bottom: 2px solid  rgb(16, 26, 205);
    display: flex;
    align-items: center;
    justify-content: center;
    color:  rgb(16, 26, 205);
    font-size: 18px;
  }
  .buttonStop {
    width: 100px;
    height: 100px;
    border-bottom: 2px solid  rgb(16, 26, 205);
    display: flex;
    align-items: center;
    justify-content: center;
    color:  rgb(16, 26, 205);
    font-size: 18px;
  }
  .buttonRight {
    width: 100px;
    height: 100px;
    border-top: 2px solid  rgb(16, 26, 205);
    border-bottom: 2px solid  rgb(16, 26, 205);
    border-right: 2px solid  rgb(16, 26, 205);
    display: flex;
    align-items: center;
    justify-content: center;
    color:  rgb(16, 26, 205);
    font-size: 18px;
  }
  
  </style>