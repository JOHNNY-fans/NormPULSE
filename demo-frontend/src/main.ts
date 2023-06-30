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

export const BASE_API = "http://0.0.0.0:2233/"
