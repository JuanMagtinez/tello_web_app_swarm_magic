<template>
  <ion-page>
    <ion-tabs>
      <ion-router-outlet></ion-router-outlet>
      <ion-tab-bar slot="bottom">

        <ion-tab-button tab="swarm" href="/Swarm/DroneSwarmPage">
          <ion-icon aria-hidden="false" :icon="airplane" />
          <ion-label>Autopilot</ion-label>
        </ion-tab-button>

        <ion-tab-button tab="AdjustDronePos" href="/Swarm/DroneSwarmAdjustPage">
          <ion-icon aria-hidden="true" :icon="hammer" />
          <ion-label>DroneAdjust</ion-label>
        </ion-tab-button>

         <ion-tab-button tab="CameraSets" href="/Swarm/CameraTest">
          <ion-icon aria-hidden="true" :icon="camera" />
          <ion-label>Camera</ion-label> 
        </ion-tab-button>

      </ion-tab-bar>
    </ion-tabs>
  </ion-page>
</template>

<script setup lang="ts">
import { IonTabBar, IonTabButton, IonTabs, IonLabel, IonIcon, IonPage, IonRouterOutlet } from '@ionic/vue';
import { airplane, bulb, camera, hammer } from 'ionicons/icons';
</script>
