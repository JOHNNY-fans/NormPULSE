<template>
  <div class="chat scrollcontent" id="scroll-chat-box">
    <!-- {{ node }} -->
    <div
      :class="item.type == 'chat-glm-norm' ? 'rtalk' : 'ptalk'"
      v-for="(item, key) in dialog_messages"
      :key="key"
    >
      <el-icon
        v-if="item.type == 'chat-glm-norm'"
        style="margin-left: 35px; font-size: 30px"
        ><IconRobort
      /></el-icon>
      <span>
        {{ item.content }}
      </span>
      <div v-if="item.type == 'chat-glm-norm'" class="tend-action">
        当前系统动作：
        <div class="emphasis">{{ item.tend }}</div>
      </div>
      <el-icon
        v-if="item.type == 'human'"
        style="margin-right: 35px; font-size: 30px"
        ><IconHuman
      /></el-icon>
    </div>
  </div>
</template>

<script setup lang="ts">
import { nextTick, ref } from "vue";
import { watch } from "vue";

interface DialogMessage {
  type: string;
  content: string;
  tend: string;
}

type HeaderProps = {
  dialog_messages: DialogMessage[];
};
const props = defineProps<HeaderProps>();
// // console.log(props);

// let series = [];
// let level_tree = ref<Record<string, Array<Record<string, TreeNode>>>>({});
// nextTick(() => {
//   let div = document.getElementById("scroll-chat-box");
//   if (div !== null) {
//     div.scrollTop = div.scrollHeight + 100;
//   }
// });
watch(
  () => props,
  () => {
    // // console.log(props.dialog_messages);
    // nextTick(() => {
    setTimeout(() => {
      let div = document.getElementById("scroll-chat-box");
      if (div !== null) {
        div.scrollTop = div.scrollHeight;
      }
    }, 100);

    // // console.log(div?.scrollTop);
    // // console.log(div?.scrollHeight);
    // });
  },
  { deep: true }
);
</script>

<style scoped>
.chat {
  width: 100%;
  /* min-height: 200px; */
  max-height: 34.25rem;
  /* float: left; */
  background-color: #fff;
  margin: 15px auto;
  /* padding: 15px; */
  /* border-left: 2px solid #b6a8ce; */
  box-shadow: 0px 4px 12px 3px rgb(42, 143, 216 / 7%);
  border-radius: 4px;
  /* height: 200px; */
  border-top: 5px solid #bbfbfc;
}
.scrollcontent {
  overflow-y: scroll;
}
.content .iconfont {
  font-size: 28px;
  margin: 0 5px;
}
.rtalk {
  margin: 5px 0;
  text-align: left;
}
.rtalk p {
  display: inline;
  margin-left: 5px;
}
.rtalk span {
  display: inline-block;
  color: #333;
  background-color: #4472c466;
  padding: 5px 10px;
  border: 1px solid #4472c4;
  border-radius: 10px;
  max-width: 80%;
  white-space: pre-wrap;
  word-wrap: break-word;
  position: relative;
  margin-left: 20px;
}
.rtalk span:before {
  position: absolute;
  content: "";
  width: 0;
  height: 0;
  right: 100%;
  bottom: 10%;
  border-top: 7px solid transparent;
  border-right: 14px solid #4472c4;
  border-bottom: 7px solid transparent;
}
.ptalk {
  margin: 5px;
  text-align: right;
  /* padding: 15px; */
}
.ptalk p {
  display: inline;
}
.ptalk span {
  display: inline-block;
  color: #333;
  background-color: #d9d2e99c;
  padding: 5px 10px;
  border: 1px solid #d9d2e9;
  border-radius: 10px;
  max-width: 80%;
  white-space: pre-wrap;
  word-wrap: break-word;
  margin-right: 20px;
  position: relative;
  text-align: left;
}
.ptalk span:after {
  position: absolute;
  content: "";
  width: 0;
  height: 0;
  left: 100%;
  bottom: 10%;
  border-top: 7px solid transparent;
  border-left: 14px solid #d9d2e9;
  border-bottom: 7px solid transparent;
}
.tend-action {
  margin: 12px 0;
  text-align: center;
  background-color: #4472c466;
}
.tend-action span {
  color: #797979;
  background-color: #ffffff;
  padding: 5px 10px;
  max-width: 200px;
  white-space: pre-wrap;
  word-wrap: break-word;
  font-size: 15px;
}
.tend-action .emphasis {
  color: #4472c4;
  font-size: 16px;
  display: inline;
  font-weight: bold;
}
</style>
