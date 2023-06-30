<template>
  <div class="bt-card">
    <div class="title" :title="title">
      {{ title }}
    </div>
    <div class="description">
      {{ description }}
    </div>
  </div>
</template>
<script setup lang="ts">
const props = defineProps<{ title: string; description: string }>();
</script>
<style scoped>
.bt-card {
  display: inline-block;
  margin: 15px;
  width: 45%;
  /* height: 200px; */
  /* height: 400px; */
}
.bt-card:hover {
  cursor: pointer;
  /* transform: translateY(30px); */
  transition: all 1s ease;
  /* background-color: #ffffff6c; */
}
.title {
  font-family: Verdana, Geneva, Tahoma, sans-serif;
  font-size: 30px;
  color: white;
  border-bottom: 1px solid #bbfbfc;
}
.bt-card:hover .title {
  transform: translateY(30px);
  transition: all 1s ease;
}
.description {
  /* display: none; */
  width: 100%;
  height: 0;
  /* padding: 10px; */
  display: flex;
  text-align: center;
  justify-content: center;
  color: #ffffff00;
  /* background-color: #ffffff6c; */
}
.bt-card:hover .description {
  width: 100%;
  min-height: 70px;
  display: flex;
  text-align: center;
  justify-content: center;
  color: #285987;
  height: 30px;
  background-color: #ffffff6c;
  transition: all 1s ease;
  font-size: 17px;
  transform: translateY(30px);
  transition: all 1s ease;
  /* line-height: 300px; */
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
