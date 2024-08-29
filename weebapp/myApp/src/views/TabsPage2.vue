<template>
  <ion-page>
    <ion-tabs>
      <ion-router-outlet></ion-router-outlet>
      <ion-tab-bar slot="bottom">

        <ion-tab-button tab="SimpleControl" href="/Simple/DroneControllPage">
          <ion-icon aria-hidden="false" :icon="airplane" />
          <ion-label>Autopilot</ion-label>
        </ion-tab-button>

        <ion-tab-button tab="SimpleVideo" href="/Simple/DroneCameraPage">
          <ion-icon aria-hidden="true" :icon="camera" />
          <ion-label>Camera</ion-label>
        </ion-tab-button>

      </ion-tab-bar>
    </ion-tabs>
  </ion-page>
</template>

<script setup lang="ts">
import { IonTabBar, IonTabButton, IonTabs, IonLabel, IonIcon, IonPage, IonRouterOutlet } from '@ionic/vue';
import { airplane, bulb, camera } from 'ionicons/icons';
</script>