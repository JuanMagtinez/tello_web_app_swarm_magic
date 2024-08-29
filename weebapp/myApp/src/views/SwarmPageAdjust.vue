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

        <div style="margin: 20px"></div>

        <div style="margin-top: 40px;">
        <div class="direction">
            <div class="buttonTurnLAdjust"></div>
            <div class="buttonForwardAdjust">
                <ion-icon :icon="arrowUp" size="large" id="forward_1" v-on:click="go($event)"/>
            </div>
            <div class="buttonTurnRAdjust"></div>
        </div>
        <div class="direction">  
            <div class="buttonLeftAdjust">
                <ion-icon :icon="arrowBack" size="large" id="left_1" v-on:click="go($event)"/>
            </div>
            <div class="buttonStopAdjust">1</div>
            <div class="buttonRightAdjust">
                <ion-icon :icon="arrowForward" size="large" id="right_1" v-on:click="go($event)"/>
            </div>
        </div>
      </div>

        <div style="margin-top: 40px;">
        <div class="direction">
            <div class="buttonTurnLAdjust"></div>
            <div class="buttonForwardAdjust">
                <ion-icon :icon="arrowUp" size="large" id="forward_2" v-on:click="go($event)"/>
            </div>
            <div class="buttonTurnRAdjust"></div>
        </div>
        <div class="direction">  
            <div class="buttonLeftAdjust">
                <ion-icon :icon="arrowBack" size="large" id="left_2" v-on:click="go($event)"/>
            </div>
            <div class="buttonStopAdjust">2</div>
            <div class="buttonRightAdjust">
                <ion-icon :icon="arrowForward" size="large" id="right_2" v-on:click="go($event)"/>
            </div>
        </div>

        <div style="margin-top: 40px;">
        <div class="direction">
            <div class="buttonTurnLAdjust"></div>
            <div class="buttonForwardAdjust">
                <ion-icon :icon="arrowUp" size="large" id="forward_3" v-on:click="go($event)"/>
            </div>
            <div class="buttonTurnRAdjust"></div>
        </div>
        <div class="direction">  
            <div class="buttonLeftAdjust">
                <ion-icon :icon="arrowBack" size="large" id="left_3" v-on:click="go($event)"/>
            </div>
            <div class="buttonStopAdjust">3</div>
            <div class="buttonRightAdjust">
                <ion-icon :icon="arrowForward" size="large" id="right_3" v-on:click="go($event)"/>
            </div>
        </div>
      </div>
      <div style="margin-top: 40px;">
        <div class="direction">
            <div class="buttonTurnLAdjust"></div>
            <div class="buttonForwardAdjust">
                <ion-icon :icon="arrowUp" size="large" id="forward_4" v-on:click="go($event)"/>
            </div>
            <div class="buttonTurnRAdjust"></div>
        </div>
        <div class="direction">  
            <div class="buttonLeftAdjust">
                <ion-icon :icon="arrowBack" size="large" id="left_4" v-on:click="go($event)"/>
            </div>
            <div class="buttonStopAdjust">4</div>
            <div class="buttonRightAdjust">
                <ion-icon :icon="arrowForward" size="large" id="right_4" v-on:click="go($event)"/>
            </div>
        </div>
      </div>
      </div>
  
      </ion-content>
    </ion-page>
  </template>
  
  <script>
  import { IonPage, IonHeader, IonToolbar, IonTitle, IonContent, IonButton, IonButtons, IonIcon } from '@ionic/vue';
  import { exit, arrowUp, arrowBack, arrowForward} from 'ionicons/icons';
  import { defineComponent, ref, onMounted } from 'vue'
  import { useMQTT } from 'mqtt-vue-hook'
  
  export default  defineComponent({
    name: 'CameraPage',
    components: { IonHeader, IonToolbar, IonTitle, IonContent, IonPage, IonButton, IonButtons, IonIcon },
  
    setup () {
      const mqttHook = useMQTT()

      function go (event) {
        const dir = event.currentTarget.id;
        const spl = dir.split("_");
        mqttHook.publish(spl[0],spl[1])   
      }
      
      return {
        arrowUp, 
        arrowBack, 
        arrowForward,
        exit,
        go
      }
    }
  });
  </script>
  
  <style>
    .buttonTurnLAdjust {
    width: 50px;
    height: 50px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: rgb(16, 26, 205);
    font-size: 18px;
  }
  .buttonForwardAdjust {
    width: 50px;
    height: 50px;
    border-top: 2px solid  rgb(16, 26, 205);
    border-left: 2px solid  rgb(16, 26, 205);
    border-right: 2px solid  rgb(16, 26, 205);
    display: flex;
    align-items: center;
    justify-content: center;
    color: rgb(16, 26, 205);
    font-size: 18px;
  }
  .buttonTurnRAdjust {
    width: 50px;
    height: 50px;
    display: flex;
    align-items: center;
    justify-content: center;
    color:  rgb(16, 26, 205);
    font-size: 18px;
  }
  .buttonLeftAdjust {
    width: 50px;
    height: 50px;
    border-top: 2px solid  rgb(16, 26, 205);
    border-left: 2px solid  rgb(16, 26, 205);
    border-bottom: 2px solid  rgb(16, 26, 205);
    display: flex;
    align-items: center;
    justify-content: center;
    color:  rgb(16, 26, 205);
    font-size: 18px;
  }
  .buttonStopAdjust {
    width: 50px;
    height: 50px;
    border-bottom: 2px solid  rgb(16, 26, 205);
    display: flex;
    align-items: center;
    justify-content: center;
    color:  rgb(16, 26, 205);
    font-size: 18px;
  }
  .buttonRightAdjust {
    width: 50px;
    height: 50px;
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