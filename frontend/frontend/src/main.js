import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import ResizeTextarea from "resize-textarea-vue3";
import ElementPlus from "element-plus";
import "element-plus/dist/index.css";
import vue3GoogleLogin from "vue3-google-login";
import Vuex from 'vuex';
import store from './store.js';



// 导入 Element Plus 的图标组件
import * as ElementPlusIconsVue from "@element-plus/icons-vue";
import "material-design-icons/iconfont/material-icons.css";

const app = createApp(App);
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component);
}

// 注册 Element Plus 的图标组件
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component);
}

const CLIENT_ID =
  "1011073193520-r2j5pttbddo2rv9d7n8pkg4646fd66h3.apps.googleusercontent.com";

app.use(vue3GoogleLogin, {
  clientId: CLIENT_ID,
  // scope: "email",
  // prompt: "consent",
});

app.use(ElementPlus);
app.use(router);
app.use(ResizeTextarea);
app.use(Vuex);
app.use(store);
app.mount("#app");
// createApp(App).use(router).mount("#app");
