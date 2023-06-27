<template>
  <main>
    <!-- <TheWelcome /> -->
    <div class="state-board">
      <TreeBoard v-if="reset" :tree="Tree" :path="path"></TreeBoard>
    </div>

    <div class="chat-board">
      <DialogBoard :dialog_messages="dialog_messages"></DialogBoard>
      <div style="width: 100%">
        <el-select v-model="tree" placeholder="选择标准库" style="width: 10%">
          <el-option :label="'ICD9-CM3'" :value="4"></el-option>
          <el-option :label="'ICD10'" :value="5"></el-option>
        </el-select>
        <el-input
          v-model="text"
          @keyup.enter="startDialog"
          style="width: 90%"
        ></el-input>
      </div>
    </div>
  </main>
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
const startDialog = async () => {
  getData(text.value, "retrieval");
  for (let i = 0; i < tree.value; i++) {
    // let last_candidate = candidates.value[candidates.value.length - 1];
    // console.log(candidates.value);
    await getData(
      prompt_dict["reference"]
        .replace("[INPUT]", text.value)
        .replace("[CANDIDATE]", candidates.value.join("，")),
      "reference",
      i
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
  //     ["霍乱（A00）", "未特指的霍乱（A00.9）"],
  //     ["麻醉药和治疗性气体的有害效应（Y48）", "局部麻醉药的有害效应（Y48.3）"],
  //     ["其他非手术性操作（99）"],
  //   ];
  // } else {
  //   path.value = [
  //     ["霍乱（A00）", "未特指的霍乱（A00.9）", "霍乱（A00.901）"],
  //     ["麻醉药和治疗性气体的有害效应（Y48）", "局部麻醉药的有害效应（Y48.3）"],
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
    content: "XXXX",
    tend: tend,
  });
  history_dialog.value.push([query, "XXXX"]);
  // path.value.push(["霍乱", "未特指的霍乱"]);
  Tree.value = TreeData;
  if (tend === "retrieval") {
    Tree.value = TreeData;
    path.value[0] = level_result[level];
  } else {
    path.value[0] = level_result[level];
    // console.log(path.value);
  }
  candidates.value = ["XXX", "XXX"];
  console.log(post_data);
  console.log(path.value);

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
  text-align: center;
  padding: 15px;
  height: 100vh;
  background-color: #f6f6f6;
  /* overflow: hidden; */
}
.state-board {
  height: 350px;
  overflow-y: scroll;
  overflow-x: hidden;
  box-shadow: 0px 4px 12px 3px rgb(43 41 83 / 7%);
  background-color: #f6f6f6;
  display: flex;
  justify-content: left;
  flex-flow: row wrap;
}
.chat-board {
  height: calc(100% - 400px);
}
</style>
