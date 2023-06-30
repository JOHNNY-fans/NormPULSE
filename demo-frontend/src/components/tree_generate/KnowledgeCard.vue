<template>
  <div v-for="(item, key) in processed_data" :key="key" class="chart">
    <el-descriptions
      class="margin-top"
      :title="ke"
      :column="2"
      :size="size"
      border
      v-for="(it, ke) in item"
      :key="ke"
    >
      <el-descriptions-item v-for="(i, k) in it" :key="k">
        <template #label>
          <div class="cell-item">
            {{ k }}
          </div>
        </template>
        {{ i }}
      </el-descriptions-item>
    </el-descriptions>
  </div>
</template>

<script setup lang="ts">
import { computed, ref, watch } from "vue";
import { nextTick } from "vue";
const size = ref<string>("");
const iconStyle = computed(() => {
  const marginMap: Record<string, string> = {
    large: "8px",
    default: "6px",
    small: "4px",
  };
  return {
    marginRight: marginMap[size.value] || marginMap.default,
  };
});
const blockMargin = computed(() => {
  const marginMap: Record<string, string> = {
    large: "32px",
    default: "28px",
    small: "24px",
  };
  return {
    marginTop: marginMap[size.value] || marginMap.default,
  };
});

const props = defineProps<{ origin_data: string[] }>();
let processed_data = ref<Record<string, Record<string, string>>[]>([]);
const processData = (origin_data: string[]) => {
  for (let i in origin_data) {
    let text = origin_data[i].replace(":", "：");
    let mention: string = text.split(" ")[0].split("：")[0];
    let cards = text.split(" ")[1].split("：");
    let cards_ = "";
    let tmp_dict: Record<any, string> = {};
    // console.log(cards);

    for (let ci in cards) {
      let next_key = cards[ci].split("。")[cards[ci].split("。").length - 1];
      console.log(next_key);
      if (cards[ci].replace(next_key, "") !== "") {
        cards_ += cards[ci].replace(next_key, "") + "##";
      }
      if (next_key !== "") {
        cards_ += next_key + "##";
      }
    }
    // console.log(cards_);

    for (let ci in cards_.split("##")) {
      if (Number(ci) % 2 === 1) {
        continue;
      }
      if (cards_.split("##")[ci] === "") {
        continue;
      }
      tmp_dict[cards_.split("##")[ci]] = cards_.split("##")[Number(ci) + 1];
    }
    console.log(tmp_dict);

    let item_dict: Record<string, Record<any, string>> = {};
    console.log(mention);

    item_dict[mention] = tmp_dict;
    processed_data.value.push(item_dict);
  }
};
nextTick(() => {
  //写入操作
  // console.log(props.path);

  processData(props.origin_data);
  console.log(processed_data.value);

  // // console.log(options.value);
});
watch(
  () => props.origin_data,
  () => {
    processData(props.origin_data);
  },
  { deep: true }
);
</script>

<style scoped>
.chart {
  /* width: 100%; */
  /* height: 315px; */
  /* float: left; */
  /* background-color: #fff; */
  /* margin: 15px auto; */
  /* padding: 15px; */
  /* border-top: none;
  border: 2px solid #bbfbfc; */
  /* border-left: 2px solid #b6a8ce; */
  /* box-shadow: 0px 4px 12px 3px rgb(43 41 83 / 7%); */
  /* border-radius: 4px; */
  /* height: 200px; */
  margin-bottom: 15px;
}
.cell-item {
  display: flex;
  align-items: center;
}
.margin-top {
  margin-top: 20px;
}
</style>
