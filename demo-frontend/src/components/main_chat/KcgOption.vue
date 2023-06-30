<template>
  <div class="state-board" v-if="!reset"></div>
  <transition name="fadet" mode="out-in">
    <div class="state-board" v-if="reset">
      <!-- <TreeBoard :tree="Tree" :path="path"></TreeBoard> -->
      <KnowledgeCard :origin_data="card_data"></KnowledgeCard>
    </div>
  </transition>
  <div class="chat-board">
    <transition name="fadet" mode="out-in">
      <DialogBoard
        :dialog_messages="dialog_messages"
        v-if="let_input || reset"
      ></DialogBoard>
    </transition>
    <transition name="fadet" mode="out-in">
      <div style="width: 100%" v-if="let_input">
        <el-select v-model="term_type" placeholder="类型" style="width: 30%">
          <el-option :label="'手术'" :value="'operation'"></el-option>
          <el-option :label="'疾病'" :value="'disease'"></el-option>
        </el-select>
        <el-input
          v-model="text"
          @keyup.enter="startDialog"
          style="width: 70%"
          placeholder="肩袖修补术"
          @click="text === '' ? (text = '肩袖修补术') : (text = text)"
        ></el-input>
      </div>
    </transition>
  </div>
  <transition name="fadet" mode="out-in">
    <div class="restart-board" v-if="let_input || reset">
      <TaskButtom
        :title="'Restart'"
        :description="'erase the current dialog'"
        @click="restart()"
      ></TaskButtom>
    </div>
  </transition>
</template>

<script setup lang="ts">
import { ref, watch, onMounted } from "vue";
import TreeData from "@/api/Tree.json";
import axios from "@/api/index";
import { BASE_API } from "@/main";

let let_input = ref(false);
let reset = ref<boolean>(false);

let text = ref("");
let term_type = ref("手术");
interface DialogMessage {
  type: string;
  content: string;
  tend: string;
}
let dialog_messages = ref<DialogMessage[]>([]);
let history_dialog = ref<string[][]>([]);
let prompt_dict = {
  dis: "知识卡片生成，请依据你掌握的医疗知识，根据输入的疾病诊断术语生成它的知识卡片，包括它的定义描述、病因、病理、部位、疾病类型和临床表现（如症状、特征、分割、分类、性别、年龄、急性慢性、发病时间等）。[INPUT]",
  op: "请通过你的医疗知识帮我完成知识卡片生成任务\n知识卡片生成，请根据我输入手术操作术语生成它的知识卡片，包括它的定义描述、手术术式、作用部位、手术入路、手术疾病性质等。[INPUT]",
};
let card_data = ref<string[]>([]);
const startDialog = async () => {
  let query =
    term_type.value === "disease"
      ? prompt_dict.dis.replace("[INPUT]", text.value)
      : prompt_dict.op.replace("[INPUT]", text.value);
  getData(query);
  text.value = "";
};
const getData = async (query: string) => {
  dialog_messages.value.push({
    type: "human",
    content: query,
    tend: "knowledge card generation",
  });

  // return;
  // TODO
  let post_data = {
    prompt: query,
    term_type: term_type.value,
    task_type: "kc",
  };
  axios.post(BASE_API + "generate", post_data).then((res: any) => {
    dialog_messages.value.push({
      type: "chat-glm-norm",
      content: res.data.model_output,
      tend: "知识卡片生成",
    });
    history_dialog.value.push([query, res.data.model_output]);
    card_data.value.push(res.data.model_output);
    reset.value = true;
  });
};
const restart = () => {
  reset.value = false;
  let_input.value = true;
  text.value = "";
  dialog_messages.value = [];
  history_dialog.value = [];
};
// beforeUnmount(() => {
//   let_input.value = false;
// });
onMounted(() => {
  console.log(let_input.value);
  setTimeout(() => {
    let_input.value = true;
  }, 800);
});
watch(
  () => let_input,
  () => {
    console.log(let_input.value);
  },
  { deep: true }
);
</script>

<style scoped>
.state-board {
  height: 40.25vh;
  overflow-y: scroll;
  overflow-x: hidden;
  box-shadow: 0px 4px 12px 3px rgb(42, 143, 216 / 7%);
  /* background-color: #181d9d; */
  display: flex;
  justify-content: left;
  flex-flow: row wrap;
  max-width: 50.25vw;
  margin: 0 auto;
  z-index: 9;
}
.chat-board {
  max-height: 40.25vh;
  max-width: 50.25vw;
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
  transform: translateY(100px);
  transition: all 1s ease;
  opacity: 0;
}
.restart-board {
  height: 18.75vw;
  width: 18.75vw;
  margin: 0 auto;
  box-shadow: 0px 4px 12px 3px rgb(42, 143, 216 / 7%);
  z-index: 9;
  text-align: center;
  position: absolute;
  bottom: 20%;
  /* transform: translateY(-50%); */
  right: 5%;
}
</style>
