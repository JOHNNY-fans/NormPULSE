<template>
  <RouterView v-if="isRouterView" />
</template>

<script setup lang="ts">
import { nextTick, provide, ref } from "vue";
let isRouterView = ref<boolean>(true);
const reload = () => {
  isRouterView.value = false;
  nextTick(() => {
    isRouterView.value = true;
  });
};
provide("reload", reload);
</script>
<style>
@import "@/assets/base.css";

#app {
  /* max-width: 1280px; */
  /* margin: 0 auto; */
  /* padding: 2rem; */
  height: 100%;
  font-weight: normal;
}
</style>
