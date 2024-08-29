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
        <ion-title class="ion-text-center">Camera</ion-title>
      </ion-toolbar>
    </ion-header>
    <ion-content :fullscreen="true">
      <div style="margin: 20px"></div>

      
      <div class="camera">
        <ion-button class="cameraButton" v-if = "!videoStream" @click="startVideoStream">Start video stream</ion-button>
        <ion-button class="cameraButton" v-if = "videoStream" @click="stopVideoStream">Stop video stream</ion-button>
      </div>
      <div style = "width:90%; margin-left:5%">
      <canvas style = "margin-left: 2%; margin-top: 20%; margin-bottom:20%; width:96%; height:100%; border-style: solid" id = "output"></canvas>
      
      </div>
    </ion-content>
  </ion-page>
</template>

<script>
import { IonPage, IonHeader, IonToolbar, IonTitle, IonContent, IonButton, IonButtons, IonIcon } from '@ionic/vue';
import { exit } from 'ionicons/icons';
import {  defineComponent, ref, onMounted } from 'vue'
import { useMQTT } from 'mqtt-vue-hook'
import * as cv from 'opencv.js'

export default  defineComponent({
  name: 'CameraPage',
  components: { IonHeader, IonToolbar, IonTitle, IonContent, IonPage, IonButton, IonButtons, IonIcon },

  setup () {
    const mode = ref('Normal');   
    const videoStream = ref(false);
    const mqttHook = useMQTT()
        
    onMounted(() => {

      const openCVFunction = {
        options: function (topic, message) {
          const img = new Image();
          img.src = "data:image/jpg;base64,"+message;
          img.onload = () => {  
          let dst = new cv.Mat();
          console.log ('mode ', mode.value)

        
          // let source = cv.imread(img);
          // cv.cvtColor(source, source, cv.COLOR_RGB2GRAY, 0);

          if (mode.value == 'Normal'){
            dst = cv.imread(img);
          }

          if (mode.value == 'Gray') {
            const mat = cv.imread(img);
            dst = new cv.Mat();
            cv.cvtColor(mat, dst, cv.COLOR_RGB2GRAY);
            mat.delete()
          }

          if (mode.value == 'Canny') {
            const mat = cv.imread(img);
            dst = new cv.Mat();
            cv.cvtColor(mat, dst, cv.COLOR_RGB2GRAY,0);
            cv.Canny(mat, dst, 50, 100, 3, false);
            mat.delete()
          }

          if(mode.value == 'Blued'){
            const mat = cv.imread(img);
            dst = new cv.Mat();
            cv.cvtColor(mat, dst, cv.COLOR_RGB2XYZ,0);
            mat.delete()
          }
  
          cv.imshow('output',dst)
          };
        }
      }
      
      mqttHook.registerEvent('videoFrame', (topic, message) => {
        console.log (message)
        openCVFunction.options(topic,message)
      })
      mqttHook.registerEvent('picture', (topic, message) => {
        openCVFunction.options(message)
      })

    })
    
    function startVideoStream () {
      mqttHook.subscribe("videoFrame", 1); 
      mqttHook.publish("StartVideoStream", "", 0)
      videoStream.value = true
      console.log ('start video') 
    }

    function stopVideoStream () {
      mqttHook.publish("StopVideoStream", "", 0)
      videoStream.value = false;
      console.log ('stop video') 
    }

    function takePicture () {
      mqttHook.publish("TakePicture", "", 0)
      mqttHook.subscribe("cameraService/mobileApp/videoFrame", 1); 
      mqttHook.publish("mobileApp/cameraService/startVideoStream", "", 1)
    }
   
    function setNormal () {
        mode.value ="Normal"
    }
    function setGrey () {
        mode.value ="Gray"
    }
    function setCanny () {
        mode.value ="Canny"
    }
    function setBlued () {
        mode.value ="Blued"
    }
    return {
      exit,
      videoStream,
      takePicture,
      startVideoStream,
      stopVideoStream,
      mode,
      mqttHook,
      setNormal,
      setBlued,
      setGrey, 
      setCanny
    }
  }
});
</script>

<style>
  .camera {
    display: flex; 
    justify-content: center
  }
  .cameraButton {
    display: flex;
    margin-top: 20px;
    width: 200px;
  }
  


</style>