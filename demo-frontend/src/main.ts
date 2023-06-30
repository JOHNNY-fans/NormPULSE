import { createApp } from "vue";
import { createPinia } from "pinia";

import App from "./App.vue";
import router from "./router";

import ECharts from "vue-echarts";
import { use } from "echarts/core";

import { CanvasRenderer } from "echarts/renderers";
import { BarChart } from "echarts/charts";
import { GridComponent, TooltipComponent } from "echarts/components";

// import VueCookies from "vue-cookies";

use([CanvasRenderer, BarChart, GridComponent, TooltipComponent]);

const app = createApp(App);

app.use(createPinia());
app.use(router);
app.component("vChart", ECharts);
app.mount("#app");

export const BASE_API =
  // "https://dsw-gateway-cn-beijing.data.aliyun.com/dsw-27313/ide/proxy/2233/"
  // "api"
  "http://localhost:2233/";
// "https://58.34.83.130:0/"
// "http://10.246.19.186:2233/"
