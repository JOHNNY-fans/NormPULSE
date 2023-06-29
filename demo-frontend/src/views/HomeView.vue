<template>
  <main>
    <transition name="fadel" mode="out-in"
      ><IconTittle
        v-if="reset"
        style="left: 0; margin: 15px"
        :title="'Norm'"
      ></IconTittle
    ></transition>
    <transition name="fader" mode="out-in"
      ><IconTittle
        v-if="reset"
        style="right: 0; margin: 15px"
        :title="'PULSE'"
      ></IconTittle
    ></transition>
    <transition name="fade" mode="out-in"
      ><IconTittle
        v-if="!reset"
        style="right: 50%; transform: translateX(50%); margin: 15px"
        :title="'NormPULSE'"
      ></IconTittle
    ></transition>

    <!-- <TheWelcome /> -->
    <div class="state-board">
      <TreeBoard v-if="reset" :tree="Tree" :path="path"></TreeBoard>
    </div>

    <div class="chat-board">
      <DialogBoard :dialog_messages="dialog_messages"></DialogBoard>
      <div style="width: 100%">
        <el-select v-model="tree" placeholder="选择标准库" style="width: 30%">
          <el-option :label="'ICD9-CM3'" :value="4"></el-option>
          <el-option :label="'ICD10'" :value="5"></el-option>
        </el-select>
        <el-input
          v-model="text"
          @keyup.enter="startDialog"
          style="width: 70%"
        ></el-input>
      </div>
    </div>
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
    <!-- <div class="wave" style="--i: 19"></div> -->
    <!-- <div class="wave" style="--i: 20"></div> -->
    <!-- <div class="container"> -->
    <!-- <div class="line" style="--x: 1; --y: 9; --z: 5"></div>
    <div class="line" style="--x: 1; --y: 4; --z: 4"></div>
    <div class="line" style="--x: 2; --y: 6; --z: 3"></div> -->
    <div class="line" style="--x: 1; --y: 4; --z: 2"></div>
    <div class="line" style="--x: 3; --y: 9; --z: 1"></div>
    <div class="line" style="--x: 1; --y: 4; --z: 0"></div>
    <div class="line" style="--x: 2; --y: 6; --z: -1"></div>
    <div class="line" style="--x: 2; --y: 8; --z: -2"></div>
    <div class="line" style="--x: 1; --y: 7; --z: -3"></div>
    <div class="line" style="--x: 1; --y: 5; --z: -4"></div>
    <div class="line" style="--x: 1; --y: 4; --z: -5"></div>
    <div class="line" style="--x: 1; --y: 7; --z: -6"></div>
    <!-- <div class="line" style="--z: 7"></div> -->
    <!-- <div class="line" style="--z: 8"></div> -->
    <!-- <div class="line" style="--z: 9"></div> -->
    <!-- <div class="line" style="--z: 10"></div> -->
    <!-- <div class="line" style="--z: 11"></div> -->
    <!-- <div class="line" style="--z: 12"></div> -->
    <!-- <div class="line" style="--z: 13"></div> -->
    <!-- <div class="line" style="--z: 14"></div> -->
    <!-- </div> -->
    <!-- <div class="clear-float" style="clear: both"></div> -->
  </main>
  <!-- <div class="decorate"></div> -->
</template>

<script setup lang="ts">
import { reactive, ref } from "vue";
import TreeData from "@/api/Tree.json";
import axios from "@/api/index";
import { BASE_API } from "@/main";

let reset = ref<boolean>(false);

let text = ref("");
let tree = ref(4);
interface TreeNode {
  code: string;
  term_name: string;
  father: string;
  child: Array<string>;
  level: number;
}
let Tree = ref<Record<string, TreeNode>>({});
let path = ref<Array<Array<string>>>([]);
let candidates = ref<Array<string>>([]);
interface DialogMessage {
  type: string;
  content: string;
  tend: string;
}
let dialog_messages = reactive<DialogMessage[]>([]);
let history_dialog = ref<string[][]>([]);
let prompt_dict = {
  retrieval: "[INPUT]",
  reference:
    "请扮演一个医学专家，你需要从候选标准术语列表中找出输入常用术语对应的标准术语，注意对应的标准术语可能有多个，你可以参考已知信息。若找到对应的标准术语则输出这些标准术语，若有多个标准术语则用'##'分隔。\n注意：1. 检查输出是否在候选术语列表中；2. 不要进行多余的解释和说明。\n常用术语：[INPUT]\n候选标准术语列表：[CANDIDATE]\n无\n输出",
};
let level_result = [
  [],
  ["肌、腱、筋膜和粘液囊手术"],
  ["肌、腱、筋膜和粘液囊手术", "肌、腱和筋膜的缝合术"],
  ["肌、腱、筋膜和粘液囊手术", "肌、腱和筋膜的缝合术", "回旋肌环带修补术"],
  [
    "肌、腱、筋膜和粘液囊手术",
    "肌、腱和筋膜的缝合术",
    "回旋肌环带修补术",
    "回旋肌环带修补术",
  ],
];
let level_output = [
  "'关节结构的修补术和整形术', '关节结构的切开术和切除术', '其他诊断性放射学和相关技术', '其他骨的切开术、切除术和切断术', '子宫和支持结构的其他手术', '心脏瓣膜和间隔手术', '手部肌、腱和筋膜手术', '淋巴系统手术', '眼眶和眼球手术', '肌、腱、筋膜和粘液囊手术', '肌肉骨骼系统的其他操作', '胸壁、胸膜、纵隔和横膈手术', '血管其他手术', '颅和周围神经的手术', '骨折和脱位复位术', '骨的其他手术'",
  "肌、腱、筋膜和粘液囊手术",
  "肌、腱和筋膜的缝合术",
  "回旋肌环带修补术",
  "回旋肌环带修补术",
];
let level_candidates = [
  [
    "关节结构的修补术和整形术",
    "关节结构的切开术和切除术",
    "其他诊断性放射学和相关技术",
    "其他骨的切开术、切除术和切断术",
    "子宫和支持结构的其他手术",
    "心脏瓣膜和间隔手术",
    "手部肌、腱和筋膜手术",
    "淋巴系统手术",
    "眼眶和眼球手术",
    "肌、腱、筋膜和粘液囊手术",
    "肌肉骨骼系统的其他操作",
    "胸壁、胸膜、纵隔和横膈手术",
    "血管其他手术",
    "颅和周围神经的手术",
    "骨折和脱位复位术",
    "骨的其他手术",
  ],
  [
    "肌、腱和筋膜的缝合术",
    "肌、腱和筋膜切断术",
    "肌、腱和筋膜其他整形术",
    "肌和腱重建术",
    "肌、腱和筋膜的其他切除术",
  ],
  [
    "腱鞘缝合术",
    "腱延迟性缝合术",
    "回旋肌环带修补术",
    "腱的其他缝合术",
    "肌肉或筋膜的其他缝合术",
  ],
  ["回旋肌环带修补术"],
];
const startDialog = async () => {
  getData(text.value, "retrieval", 0);
  for (let i = 0; i < tree.value; i++) {
    // let last_candidate = candidates.value[candidates.value.length - 1];
    // console.log(candidates.value);
    await getData(
      prompt_dict["reference"]
        .replace("[INPUT]", text.value)
        .replace("[CANDIDATE]", candidates.value.join("，")),
      "reference",
      i + 1
    );
  }
};
const getData = async (query: string, tend: string, level: number) => {
  // fetch(query).then((res) => {
  // Tree.value = TreeData;
  // let switch_num = Math.random();
  // if (switch_num < 0.3) {
  //   path.value = [
  //     ["霍乱（A00）"],
  //     ["麻醉药和治疗性气体的有害效应（Y48）"],
  //     ["其他非手术性操作（99）"],
  //   ];
  // } else if (switch_num > 0.3 && switch_num < 0.7) {
  //   path.value = [
  //     ["霍乱（A00）","未特指的霍乱（A00.9）"],
  //     ["麻醉药和治疗性气体的有害效应（Y48）","局部麻醉药的有害效应（Y48.3）"],
  //     ["其他非手术性操作（99）"],
  //   ];
  // } else {
  //   path.value = [
  //     ["霍乱（A00）","未特指的霍乱（A00.9）","霍乱（A00.901）"],
  //     ["麻醉药和治疗性气体的有害效应（Y48）","局部麻醉药的有害效应（Y48.3）"],
  //     ["其他非手术性操作（99）"],
  //   ];
  // }

  dialog_messages.push({
    type: "human",
    content: query,
    tend: "human",
  });
  let post_data = {
    input: query,
    history: history_dialog.value,
  };
  dialog_messages.push({
    type: "chat-glm-norm",
    content: level_output[level],
    tend: tend,
  });
  history_dialog.value.push([query, level_output[level]]);
  // path.value.push(["霍乱","未特指的霍乱"]);
  Tree.value = TreeData;
  if (tend === "retrieval") {
    Tree.value = TreeData;
    path.value[0] = level_result[level];
  } else {
    path.value[0] = level_result[level];
    // console.log(path.value);
  }
  candidates.value = level_candidates[level];
  // console.log(post_data);
  // console.log(path.value);

  reset.value = true;
  return;
  // TODO
  await axios.post(BASE_API + "chat", post_data).then((res: any) => {
    dialog_messages.push({
      type: "chat-glm-norm",
      content: res.data.output,
      tend: tend,
    });
    history_dialog.value.push([query, res.data.output]);
    if (tend === "retrieval") {
      Tree.value = TreeData;
      reset.value = true;
    } else {
      path.value.push(res.data.output);
    }
    candidates.value = res.data.candidate;
  });
};
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
.state-board {
  height: 350px;
  overflow-y: scroll;
  overflow-x: hidden;
  box-shadow: 0px 4px 12px 3px rgb(42, 143, 216 / 7%);
  /* background-color: #181d9d; */
  display: flex;
  justify-content: left;
  flex-flow: row wrap;
  max-width: 900px;
  margin: 0 auto;
  z-index: 9;
}
.chat-board {
  max-height: 35.25rem;
  max-width: 900px;
  margin: 0 auto;
  box-shadow: 0px 4px 12px 3px rgb(42, 143, 216 / 7%);
  z-index: 9;
}
.fade-enter-active,
.fade-leave-active {
  transition: all 1s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.fadel-leave-active {
  transform: translateX(-100px);
  transition: all 1s ease;
}
.fadel-enter-from,
.fadel-leave-to {
  transform: translateX(100px);
  opacity: 0;
}

.fader-leave-active {
  transform: translateX(100px);
  transition: all 1s ease;
}
.fader-enter-from,
.fader-leave-to {
  transform: translateX(-100px);
  opacity: 0;
}
</style>
