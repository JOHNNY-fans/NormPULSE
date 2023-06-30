<template>
  <div class="state-board" v-if="!reset">
    <!-- <TreeBoard :tree="Tree" :path="path"></TreeBoard> -->
  </div>
  <transition name="fadet" mode="out-in">
    <div class="state-board" v-if="reset">
      <TreeBoard :tree="Tree" :path="path"></TreeBoard>
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
        <el-select v-model="tree" placeholder="选择标准库" style="width: 30%">
          <el-option :label="'ICD9-CM3'" :value="'operation'"></el-option>
          <el-option :label="'ICD10'" :value="'disease'"></el-option>
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
    <transition name="fadet" mode="out-in">
      <div style="width: 100%" v-if="!let_input && reset">
        <ActionButtom
          :title="'Go on'"
          :description="'Go on reference with current answer'"
          @click="continueAnswer"
        ></ActionButtom>
        <ActionButtom
          :title="'Fix'"
          :description="'Fix the error answer if possible'"
          @click="handleOpen"
        ></ActionButtom>
        <!-- <el-button type="primary" @click="continueAnswer">Go on</el-button>
        <el-button type="warning" @click="handleOpen">Fix</el-button> -->
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
  <el-dialog
    v-model="dialogVisible"
    title="Tips"
    width="30%"
    :before-close="handleClose"
  >
    <el-checkbox-group v-model="target_answers">
      <el-checkbox :label="item" v-for="(item, key) in candidates" :key="key" />
    </el-checkbox-group>
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="dialogVisible = false">Cancel</el-button>
        <el-button type="primary" @click="fixAnswer()"> Confirm </el-button>
      </span>
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
import { ref, watch, onMounted } from "vue";
import TreeData from "@/api/Tree.json";
import axios from "@/api/index";
import { BASE_API } from "@/main";

let let_input = ref(false);
let reset = ref<boolean>(false);
let level = ref<number>(1);

let text = ref("");
let tree = ref("operation");
let tree_depth = ref(4);
let nop_n = ref(200);
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
let answer = ref<string>("");
interface DialogMessage {
  type: string;
  content: string;
  tend: string;
}
let dialog_messages = ref<DialogMessage[]>([]);
let history_dialog = ref<string[][]>([]);
let prompt_dict = {
  retrieval: "[INPUT]",
  reference:
    "请扮演一个医学专家，你需要从候选标准术语列表中找出输入常用术语对应的标准术语，注意对应的标准术语可能有多个。若找到对应的标准术语则输出这些标准术语，有多个标准术语则用'##'分隔；若找不到对应的标准术语则输出“无对应标准术语”，并推荐可能对应的标准术语。\n注意：1. 保证输出的标准术语是否在候选术语列表中；2. 不要进行多余的解释和说明\n常用术语：[INPUT]\n候选标准术语列表：\n[CANDIDATE]\n输出",
};
const startDialog = async () => {
  await retrievalData(text.value);
  // await inferenceData(text.value);
  let_input.value = false;
  reset.value = true;
};
const fixAnswer = async () => {
  level.value -= 1;
  // retrievalData(new_target);
  answer.value = target_answers.value.join("##");
  dialog_messages.value[dialog_messages.value.length - 1].content =
    answer.value;
  // await inferenceData(answer.value);
};
const continueAnswer = async () => {
  await retrievalData(text.value);
  // await inferenceData(answer.value);
};
const retrievalData = async (query: string) => {
  dialog_messages.value.push({
    type: "human",
    content: query,
    tend: "human",
  });
  let post_data = {
    term_type: tree.value,
    topN: nop_n.value,
    mention: query,
    level: level.value,
    history: history_dialog.value,
  };
  axios.post(BASE_API + "retrival", post_data).then((res: any) => {
    // Tree.value.push(res.data.cand);
    tree_depth.value = res.data.max_depth;
    candidates.value = [];
    for (let i in res.data.cand) {
      Tree.value[res.data.cand[i].code] = res.data.cand[i];
      candidates.value.push(res.data.cand[i]["term_name"]);
    }
    dialog_messages.value.push({
      type: "chat-glm-norm",
      content: candidates.value.join("；"),
      tend: "Retrieval" + "（第" + String(level.value) + "层）",
    });
    inferenceData(query);
  });
};
const inferenceData = async (query: string) => {
  let prompt = prompt_dict["reference"]
    .replace("[INPUT]", query)
    .replace("[CANDIDATE]", candidates.value.join("\n"));
  dialog_messages.value.push({
    type: "human",
    content: prompt_dict["reference"].replace("[INPUT]", query),
    tend: "human",
  });
  let post_data = {
    prompt: prompt,
    term_type: tree.value,
    task_type: "norm",
  };
  axios.post(BASE_API + "generate", post_data).then((res: any) => {
    dialog_messages.value.push({
      type: "chat-glm-norm",
      content: res.data.model_output,
      tend: "Inference" + "（第" + String(level.value) + "层）",
    });
    history_dialog.value.push([query, res.data.model_output]);
    path.value = res.data.inference_answer_path;
    answer.value = res.data.model_output;
    level.value += 1;
  });
};
const restart = () => {
  reset.value = false;
  tree_depth.value = 0;
  Tree.value = {};
  let_input.value = true;
  text.value = "";
  path.value = [];
  candidates.value = [];
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

const dialogVisible = ref(false);
let target_answers = ref<string[]>([]);
const handleOpen = () => {
  dialogVisible.value = true;
};
const handleClose = () => {
  dialogVisible.value = false;
};
</script>

<style scoped>
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
  height: 300px;
  width: 300px;
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
