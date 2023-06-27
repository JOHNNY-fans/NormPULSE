<template>
  <vChart
    class="chart"
    :option="item"
    ref="myChart"
    v-for="(item, key) in options"
    :key="key"
  >
    <!-- {{ node }} -->
  </vChart>
</template>

<script setup lang="ts">
import { use } from "echarts/core";
import {
  TitleComponent,
  TooltipComponent,
  ToolboxComponent,
} from "echarts/components";
import { TreeChart } from "echarts/charts";
import { CanvasRenderer } from "echarts/renderers";
import { ref } from "vue-demi";
import { nextTick } from "vue";
import vChart from "vue-echarts";
import { watch } from "vue";

{
  vChart;
}

use([
  TitleComponent,
  TooltipComponent,
  TreeChart,
  CanvasRenderer,
  ToolboxComponent,
]);

interface TreeNode {
  code: string;
  term_name: string;
  father: string;
  child: Array<string>;
  level: number;
}
interface chartNode {
  name: string;
  children: Array<chartNode> | undefined;
  itemStyle: Record<string, string>;
  lineStyle: Record<string, string | number>;
  label: Record<string, string | number>;
}
const props =
  defineProps<{ tree: Record<string, TreeNode>; path: Array<Array<string>> }>();
// let series = [];
// let level_tree = ref<Record<string, Array<Record<string, TreeNode>>>>({});
let highlignt_color = "#4472c4";
let normal_color = "#cccccc";
let highlight_font_size = 14;
let normal_font_size = 12;
const lookForChildren = (father_code: string) => {
  let children_list: chartNode[] = [];
  if (
    props.tree[father_code].child == null ||
    props.tree[father_code].child.length == 0
  ) {
    return [];
  } else {
    for (let i in props.tree[father_code].child) {
      let color = normal_color;
      let font_size = normal_font_size;
      let formatter = [
        `{a|${props.tree[props.tree[father_code].child[i]].term_name}}`,
        `{b|${
          "（" + props.tree[props.tree[father_code].child[i]].code + "）"
        }}`,
      ].join("\n");
      if (
        props.path
          .flat(Infinity)
          .includes(props.tree[props.tree[father_code].child[i]].term_name)
      ) {
        color = highlignt_color;
        font_size = highlight_font_size;
        formatter = [
          `{c|${props.tree[props.tree[father_code].child[i]].term_name}}`,
          `{d|${
            "（" + props.tree[props.tree[father_code].child[i]].code + "）"
          }}`,
        ].join("\n");
      }
      children_list.push({
        name: props.tree[props.tree[father_code].child[i]].term_name,
        children: lookForChildren(props.tree[father_code].child[i]),
        itemStyle: {
          color: color,
          // borderJoin: "round",
        },
        label: {
          fontSize: font_size,
          borderColor: color,
          formatter: formatter,
        },
        lineStyle: {
          color: color,
          // curveness: 111,
        },
      });
      console.log(children_list);
    }
    return children_list;
  }
};
const processData = () => {
  let data: chartNode[] = [];
  // console.log(props.tree);
  // let index = 0;
  for (let key in props.tree) {
    if (props.tree[key].father == null || props.tree[key].father == "无") {
      let child_codes = props.tree[key].child;
      let tmp_children: chartNode[] = [];
      // while (child_codes != null && child_codes?.length > 0) {
      for (let i in child_codes) {
        if (props.tree[child_codes[i]] == undefined) {
          console.log(child_codes[i]);

          continue;
        }
        let color = normal_color;
        let font_size = normal_font_size;
        let formmater = [
          `{a|${props.tree[child_codes[i]].term_name}}`,
          `{b|${"（" + props.tree[child_codes[i]].code + "）"}}`,
        ].join("\n");
        // // console.log(props.path, index, props.path[index]);

        if (
          props.path
            .flat(Infinity)
            .includes(props.tree[child_codes[i]].term_name)
        ) {
          color = highlignt_color;
          font_size = highlight_font_size;
          formmater = [
            `{c|${props.tree[child_codes[i]].term_name}}`,
            `{d|${"（" + props.tree[child_codes[i]].code + "）"}}`,
          ].join("\n");
        }
        tmp_children.push({
          name: props.tree[child_codes[i]].term_name,
          children: lookForChildren(props.tree[child_codes[i]].code),
          itemStyle: {
            color: color,
            // borderJoin: "round",
          },
          label: {
            fontSize: font_size,
            borderColor: color,
            formatter: formmater,
          },
          lineStyle: {
            color: color,
            // curveness: 111,
          },
        });
        // console.log(tmp_children);
      }
      // }
      let color = normal_color;
      let font_size = normal_font_size;
      let formmater = [
        `{a|${props.tree[key].term_name}}`,
        `{b|${"（" + props.tree[key].code + "）"}}`,
      ].join("\n");
      if (props.path.flat(Infinity).includes(props.tree[key].term_name)) {
        color = highlignt_color;
        font_size = highlight_font_size;
        formmater = [
          `{c|${props.tree[key].term_name}}`,
          `{d|${"（" + props.tree[key].code + "）"}}`,
        ].join("\n");
      }
      data.push({
        name: props.tree[key].term_name,
        children: tmp_children,
        itemStyle: {
          color: color,
          // borderJoin: "round",
        },
        label: {
          fontSize: font_size,
          borderColor: color,
          formatter: formmater,
        },
        lineStyle: {
          color: color,
          // curveness: 111,
        },
      });
      // index++;
      // // // console.log(index);
    }
  }
  // console.log(data);
  let options = [];
  for (let i in data) {
    options.push({
      tooltip: {
        trigger: "item",
        triggerOn: "mousemove",
      },
      series: {
        type: "tree",
        data: [data[i]],
        top: "1%",
        left: "7%",
        bottom: "1%",
        right: "20%",
        symbol: "none",
        // symbolSize: 17,
        // symbolOffset: [-15, 7],
        // edgeShape: "polyline",
        // edgeForkPosition: "50%",
        roam: true,
        itemStyle: {
          borderWidth: 122,
          borderCap: "round",
        },
        lineStyle: {
          width: 7,
        },
        label: {
          position: "right",
          verticalAlign: "middle",
          align: "left",
          fontSize: 13,
          backgroundColor: "#fff",
          borderWidth: 3,
          padding: 5,
          borderRadius: 10,
          offset: [-10, 0],

          rich: {
            a: {
              color: normal_color,
              fontSize: highlight_font_size,
            },
            b: {
              color: normal_color,
              fontSize: normal_font_size,
            },
            c: {
              color: highlignt_color,
              fontSize: highlight_font_size,
            },
            d: {
              color: highlignt_color,
              fontSize: normal_font_size,
            },
          },
        },

        leaves: {
          label: {
            position: "right",
            verticalAlign: "middle",
            align: "left",
          },
        },

        emphasis: {
          focus: "descendant",
          itemStyle: {
            color: highlignt_color,
          },
          lineStyle: {
            color: highlignt_color,
          },
        },

        expandAndCollapse: true,

        animationDuration: 550,
        animationDurationUpdate: 750,
      },
    });
  }
  console.log(options);

  return options;
};
let options = ref(processData());
nextTick(() => {
  //写入操作
  // console.log(props.path);

  options.value = processData();
  // // console.log(options.value);
});
watch(
  () => props.path,
  () => {
    options.value = processData();
  },
  { deep: true }
);
</script>

<style scoped>
.chart {
  width: 100%;
  height: 315px;
  /* float: left; */
  background-color: #fff;
  margin: 15px auto;
  padding: 15px;
  border-top: 5px solid #bbfbfc;
  border: 5px solid #bbfbfc;
  /* border-left: 2px solid #b6a8ce; */
  /* box-shadow: 0px 4px 12px 3px rgb(43 41 83 / 7%); */
  border-radius: 4px;
  /* height: 200px; */
}
</style>
