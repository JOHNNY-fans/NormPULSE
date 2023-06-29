<template>
  <div class="title" :title="title">{{ title }}</div>
</template>
<script setup lang="ts">
const props = defineProps<{ title: string }>();
</script>
<style scoped>
.title {
  font-family: Verdana, Geneva, Tahoma, sans-serif;
  height: 150px;
  font-size: 150px;
  line-height: 150px;
  /* float: left; */
  position: absolute;
  top: 10%;
  transition: all 3s cubic-bezier(0.075, 0.82, 0.165, 1);
  background-image: linear-gradient(to bottom, #285987, #6fa7da);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  -webkit-box-reflect: below -33px linear-gradient(transparent, rgba(0, 0, 0, 0.2));
}
/* .title::before {
  content: attr(title);
  position: absolute;
  z-index: 1;
  top: 100%;
  left: 0;
  height: 100%;
  width: 100%;
  transform: scaleY(-1);
} */
/* .title::after {
  content: "";
  position: absolute;
  z-index: 1;
  top: 100%;
  background: linear-gradient(to bottom, #366a99, #6fa5d800);
} */
</style>
