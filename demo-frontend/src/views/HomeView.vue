<template>
  <main>
    <transition name="fadel" mode="out-in"
      ><IconTittle
        v-show="task_type !== ''"
        style="left: 0; margin: 15px"
        :title="'Norm'"
      ></IconTittle
    ></transition>
    <transition name="fader" mode="out-in"
      ><IconTittle
        v-show="task_type !== ''"
        style="right: 0; margin: 15px"
        :title="'PULSE'"
      ></IconTittle
    ></transition>
    <transition name="fade" mode="out-in"
      ><IconTittle
        v-show="task_type === ''"
        style="right: 50%; transform: translateX(50%); margin: 15px"
        :title="'NormPULSE'"
      ></IconTittle
    ></transition>

    <!-- <TheWelcome /> -->
    <transition name="fadet" mode="out-in">
      <div class="choose-board" v-show="task_type === ''">
        <TaskButtom
          :title="'Knowledge Card Generation'"
          :description="'Generate knowledge card for given mention.'"
          @click="chooseCard('KCG')"
        ></TaskButtom>
        <TaskButtom
          :title="'Hierarchical Normalization'"
          :description="'Auto inference Normalization'"
          @click="chooseCard('HN')"
        ></TaskButtom>
      </div>
    </transition>
    <transition name="fadet" mode="out-in">
      <div class="divider" v-show="task_type === ''"></div>
    </transition>
    <transition name="fadet" mode="out-in">
      <NormOption v-if="task_type === 'HN'"></NormOption>
    </transition>
    <transition name="fadet" mode="out-in">
      <KcgOption v-if="task_type === 'KCG'"></KcgOption>
    </transition>
    <transition name="fadet" mode="out-in">
      <div class="restart-board" v-show="task_type !== ''">
        <TaskButtom
          :title="'Goback'"
          :description="'Choose the task again'"
          @click="chooseCard('')"
        ></TaskButtom>
      </div>
    </transition>
    <div class="wave" style="--i: 0"></div>
    <div class="wave" style="--i: 1"></div>
    <div class="wave" style="--i: 2"></div>
    <div class="wave" style="--i: 3"></div>
    <div class="wave" style="--i: 4"></div>
    <div class="wave" style="--i: 5"></div>
    <div class="wave" style="--i: 6"></div>
    <div class="wave" style="--i: 7"></div>
    <div class="wave" style="--i: 8"></div>
    <div class="wave" style="--i: 9"></div>
    <div class="wave" style="--i: 10"></div>
    <div class="wave" style="--i: 11"></div>
    <div class="wave" style="--i: 12"></div>
    <div class="wave" style="--i: 13"></div>
    <div class="wave" style="--i: 14"></div>
    <div class="wave" style="--i: 15"></div>
    <div class="wave" style="--i: 16"></div>
    <div class="wave" style="--i: 17"></div>
    <div class="wave" style="--i: 18"></div>
    <div class="line" style="--x: 1; --y: 4; --z: 2"></div>
    <div class="line" style="--x: 3; --y: 9; --z: 1"></div>
    <div class="line" style="--x: 1; --y: 4; --z: 0"></div>
    <div class="line" style="--x: 2; --y: 6; --z: -1"></div>
    <div class="line" style="--x: 2; --y: 8; --z: -2"></div>
    <div class="line" style="--x: 1; --y: 7; --z: -3"></div>
    <div class="line" style="--x: 1; --y: 5; --z: -4"></div>
    <div class="line" style="--x: 1; --y: 4; --z: -5"></div>
    <div class="line" style="--x: 1; --y: 7; --z: -6"></div>
  </main>
  <!-- <div class="decorate"></div> -->
</template>

<script setup lang="ts">
import { reactive, ref, watch, inject } from "vue";
import TreeData from "@/api/Tree.json";
import axios from "@/api/index";
import { BASE_API } from "@/main";
const reload = inject("reload", Function, true);
let task_type = ref("");
// let let_input = ref(false);
const chooseCard = (type: string) => {
  task_type.value = type;
  setTimeout(() => {
    if (type === "") {
      reload();
    }
  }, 500);
};
watch(
  () => task_type,
  () => {
    console.log(task_type.value);
  },
  { deep: true }
);
// getData(text.value);
</script>

<style scoped>
main {
  overflow: auto;
  text-align: center;
  /* padding: 15px; */
  height: 100vh;
  max-height: 100vh;
  width: 100vw;
  /* overflow: auto; */
  /* background-color: #f6f6f6; */
  background-image: linear-gradient(
    to bottom right,
    #040710,
    #040710,
    #0d1748,
    #0d1748,
    #0c1540
  );
  position: relative;
  perspective: 800px;
  perspective-origin: left bottom;
  transform-style: preserve-3d;
  /* animation: wave-light infinite; */
}
.wave {
  z-index: 1;
  width: 100%;
  height: 20vh;
  position: absolute;
  /* position: fixed; */
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  /* background-color: #fff;
  background-image: url("/src/assets/pulse.png");
  background-size: contain; */
  border-radius: 100%;
  border: 2px solid #6277f0;
  animation: wave-light 10s infinite;
  animation-delay: calc(var(--i) * 0.5s);
}
@keyframes wave-light {
  0% {
    width: 0;
    height: 0;
    opacity: 1;
  }
  50% {
    opacity: 1;
    transform: translateX(-50%);
  }
  100% {
    width: 100vw;
    height: 20vh;
    opacity: 0;
    transform: translateX(-50%);
  }
}
.line {
  z-index: 1;
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
  top: 0;
  right: 25%;
  /* transform: translateZ(calc(var(--z)) * 100px); */
  /* bottom: 0; */
  width: 200px;
  height: 3px;
  border-radius: 3px;
  /* background-color: #fff; */
  background-image: linear-gradient(to right, #6be6f7, #6be6f750, transparent);
  animation: down 5s infinite linear both;
  animation-delay: calc(var(--z) * 3s);
  opacity: 0;
}
@keyframes down {
  0% {
    transform: translateY(calc(var(--y) * 30px))
      translateZ(calc(var(--z) * 120px)) translateX(calc(var(--x) * 200px))
      rotate(-45deg);
    opacity: 0;
  }
  100% {
    transform: translateY(calc(var(--y) * 100px))
      translateZ(calc(var(--z) * 120px)) translateX(calc(var(--x) * -100px))
      rotate(-45deg);
    opacity: 1;
  }
}
.line::before,
.line::after {
  position: absolute;
  content: "";
  width: inherit;
  height: inherit;
  background-image: inherit;
}
.line::before {
  filter: blur(5px);
}
.line::after {
  filter: blur(15px);
}
.choose-board {
  height: 300px;
  width: 1500px;
  margin: 0 auto;
  box-shadow: 0px 4px 12px 3px rgb(42, 143, 216 / 7%);
  z-index: 9;
  text-align: center;
  position: absolute;
  top: 40%;
  /* transform: translateY(-50%); */
  left: 50%;
  transform: translateX(-50%);
}
.restart-board {
  height: 300px;
  width: 300px;
  margin: 0 auto;
  box-shadow: 0px 4px 12px 3px rgb(42, 143, 216 / 7%);
  z-index: 9;
  text-align: center;
  position: absolute;
  bottom: 20%;
  /* transform: translateY(-50%); */
  left: 5%;
  /* transform: translateX(-50%); */
}
.divider {
  border-top: 5px solid #bbfbfc;
  width: 900px;
  height: 1px;
  position: absolute;
  top: 60%;
  /* transform: translateY(-50%); */
  left: 50%;
  transform: translateX(-50%);
  z-index: 8;
}

.fade-enter-active,
.fade-leave-active {
  transition: all 1s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* .fadel-enter-active, */
.fadel-leave-active {
  transform: translateX(-300px);
  transition: all 1s ease;
}
.fadel-enter-from,
.fadel-leave-to {
  transform: translateX(100px);
  opacity: 0;
}

/* .fader-enter-active, */
.fader-leave-active {
  transform: translateX(300px);
  transition: all 1s ease;
}
.fader-enter-from,
.fader-leave-to {
  transform: translateX(-100px);
  opacity: 0;
}

.fadet-enter-active,
.fadet-leave-active {
  transition: all 1s ease;
}
.fadet-enter-from,
.fadet-leave-to {
  /* transform: translateY(-100px); */
  height: 0;
  transition: all 1s ease;
  opacity: 0;
}
</style>
