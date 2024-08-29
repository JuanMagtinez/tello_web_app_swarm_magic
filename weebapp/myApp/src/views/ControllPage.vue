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
          <ion-menu-button :auto-hide="true"></ion-menu-button>
        </ion-buttons>

        <ion-title class="ion-text-center" text-align: center>Autopilot</ion-title>

      </ion-toolbar>
    </ion-header>
    <ion-content>

      <div style="margin: 20px">
        <label style="margin-right: 10px;">Drone battery:</label>
        <ion-icon v-if = "battery<20" :icon="batteryDead" color="red"/>
        <ion-icon v-if = "battery<=70 && battery>=20" :icon="batteryHalf"/>
        <ion-icon v-if = "battery>70" :icon="batteryFull"/>
        <label style="margin-left: 10px;">{{ battery }} %</label>
      </div>

      <div style="margin: 20px"></div>

      <div class="autopilot">
        <ion-button v-if = "!flying && !takingOff" class="autopilotButton" @click="takeOff">Take Off</ion-button>
        <ion-button  @click="takeOff">FLIP!</ion-button>
        <ion-button :disabled="flying" v-if = "flying" color="success" class="autopilotButton">Flying</ion-button>
        <ion-button :disabled="takingOff"  v-if = "takingOff" color="warning" class="autopilotButton">Taking Off</ion-button>
      </div>
      <div class="autopilot">
        <ion-button :disabled="!flying || landing" class="autopilotButton" @click="land">Land</ion-button>
      </div>
      
      <div style="margin-top: 40px;">
        <div class="direction">

          <div v-if = "direction != 'TLeft'" id="TLeft" v-on:click="go($event)" class="box">
            Turn Left</div>
          <div v-if = "direction == 'TLeft'" id="TLeft" v-on:click="go($event)" class="box2">
            Turn Left</div>

          <div v-if = "direction != 'forward'" id="forward" v-on:click="go($event)" class="box">
            <ion-icon :icon="arrowUp" size="large" /></div>
          <div v-if = "direction == 'forward'" id="forward" v-on:click="go($event)" class="box2">
            <ion-icon :icon="arrowUp" size="large" /></div>

          <div v-if = "direction != 'TRight'" id="TRight" v-on:click="go($event)" class="box">
            Turn Right</div>
          <div v-if = "direction == 'TRight'" id="TRight" v-on:click="go($event)" class="box2">
            Turn Right</div>
        </div>
        <div class="direction">  
          
          <div v-if = "direction != 'left'" id="left" v-on:click="go($event)" class="box">
            <ion-icon :icon="arrowBack" size="large" /></div>
          <div v-if = "direction == 'left'" id="left" v-on:click="go($event)" class="box2">
            <ion-icon :icon="arrowBack" size="large" /></div>

          <div v-if = "direction != 'stop'" id="stop" v-on:click="go($event)" class="box">
            STOP</div>
          <div v-if = "direction == 'stop'" id="stop" v-on:click="go($event)" class="box2">
            STOP</div>

          <div v-if = "direction != 'right'" id="right" v-on:click="go($event)" class="box">
            <ion-icon :icon="arrowForward" size="large" /></div>
          <div v-if = "direction == 'right'" id="right" v-on:click="go($event)" class="box2">
            <ion-icon :icon="arrowForward" size="large" /></div>

        </div>
        <div class="direction">
          <div v-if = "direction != 'up'" id="up" v-on:click="go($event)" class="box">
            Up</div>
          <div v-if = "direction == 'up'" id="up" v-on:click="go($event)" class="box2">
            Up</div>

          <div v-if = "direction != 'back'" id="back" v-on:click="go($event)" class="box">
            <ion-icon :icon="arrowDown" size="large" /></div>
          <div v-if = "direction == 'back'" id="back" v-on:click="go($event)" class="box2">
            <ion-icon :icon="arrowDown" size="large" /></div>

          <div v-if = "direction != 'down'" id="down" v-on:click="go($event)" class="box">
            Down</div>
          <div v-if = "direction == 'down'" id="down" v-on:click="go($event)" class="box2">
            Down</div>
        </div>
      </div>


      <ion-header collapse="condense">
        <ion-toolbar>
          <ion-title size="large"></ion-title>
        </ion-toolbar>
      </ion-header>

    </ion-content>
  </ion-page>
</template>

<script>
import { defineComponent, ref, onMounted } from 'vue';
import { IonPage, IonHeader, IonToolbar, IonTitle, IonContent, IonIcon, alertController, IonButtons, IonMenuButton,} from '@ionic/vue';
import { arrowUp, arrowBack, arrowForward, arrowDown, exit, batteryDead, batteryHalf, batteryFull } from 'ionicons/icons';
import { useMQTT } from 'mqtt-vue-hook' 

export default  defineComponent({
  name: 'AutopilotDronePage',
  components: { IonPage, IonHeader, IonToolbar, IonTitle, IonContent, IonIcon, IonButtons, IonMenuButton},

  setup() {

    const flying = ref(false);
    const takingOff = ref(false);
    const landing = ref(false);
    const direction = ref(undefined);
    const battery = ref(0);
    const mqttHook = useMQTT();
    
    const interval = setInterval(() => {
      mqttHook.publish('state','',1);
    }, 5000);

    function takeOff(){
      // mqttHook.publish('stop','',1);
      mqttHook.publish('takeoff','',1);
      // flying.value = true;
      takingOff.value = true;
    }

    function land(){
      mqttHook.publish('land','',1);
      // flying.value = false;
      landing.value = true;
      direction.value = undefined;
    }

    function go (event) {
      if (!flying.value){
        presentAlert();
      } else {
        const dir = event.currentTarget.id;
        direction.value = dir;
        mqttHook.publish(dir,'',1);
        console.log(dir);
      }
    }

    const presentAlert = async () => {
      const alert = await alertController.create({
        header: 'Alert',
        subHeader: 'Not flying!',
        message: 'You must take off in order to move freely.',
        buttons: ['OK'],
      });
      await alert.present();
    };

    const outOfRangeAlert = async () => {
      const alert = await alertController.create({
        header: 'Alert',
        subHeader: 'Out of Range!',
        message: "You can't fly any further, you'll have to try another direction... ",
        buttons: ['OK'],
      });
      await alert.present();
    };

    onMounted (()=>{
      mqttHook.subscribe('battery', 1);
      mqttHook.registerEvent('battery', (topic, message) => {
        battery.value = message;
      });
      mqttHook.subscribe('height', 1);
      mqttHook.registerEvent('height', (topic, message) => {
        const h = JSON.parse(message);
        // console.log(h);
        if (h == 0){
          flying.value = false;
          takingOff.value = false;
          landing.value = false;
        }
      });
      mqttHook.subscribe('flyingState', 1);
      mqttHook.registerEvent('flyingState', (topic, message) => {
        // console.log(topic);
        const data = JSON.parse(message);
        // 1=flying   0=landing
        if (data == 1){
          console.log('flying');
          flying.value = true;
          takingOff.value = false;
        }
        else if (data == 0){
          console.log('on land');
          flying.value = false;
          landing.value = false;
        }
        
      });
      mqttHook.subscribe('direction', 1);
      mqttHook.registerEvent('direction', (topic,message) => {
        console.log(topic);
        const dat = JSON.parse(message);
        console.log(dat);
        if (dat == 1){
          direction.value = undefined;
        }
        else if (dat == 0){
          direction.value = undefined;
          outOfRangeAlert();
        }
      });
    })

    return {
      takeOff,
      flying,
      takingOff,
      landing,
      land,
      direction,
      go, 
      arrowUp, 
      arrowBack, 
      arrowForward, 
      arrowDown,
      exit,
      batteryDead,
      batteryHalf,
      batteryFull,
      battery,
      interval,      
    }
  }
});

</script>

<style>
  .autopilot {
    display: flex; 
    justify-content: center
  }
  .autopilotButton {
    display: flex;
    margin-top: 20px;
    width: 180px;
  }
  .direction {
    display: flex;
    justify-content: center;

  }
  .box {
    width: 100px;
    height: 100px;
    background: #444;
    border: 2px solid rgb(28, 81, 5);
    display: flex;
    align-items: center;
    justify-content: center;
    color: yellowgreen;
    font-size: 18px;
    margin: 5px
  }
  .box2 {
    width: 100px;
    height: 100px;
    background: #2c2b2b;
    border: 2px solid rgb(28, 81, 5);
    display: flex;
    align-items: center;
    justify-content: center;
    color: yellowgreen;
    font-size: 18px;
    margin: 5px
  }

  
</style>