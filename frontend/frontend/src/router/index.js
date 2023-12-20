import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";

const routes = [
  {
    path: "/",
    name: "home",
    component: HomeView,
  },
  {
    path: "/about",
    name: "about",
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () =>
      import(/* webpackChunkName: "about" */ "../views/AboutView.vue"),
  },
  {
    path: "/calender",
    name: "calender",
    component: () => import("../views/Calender.vue"),
  },
  {
    path: "/tim",
    name: "tim",
    component: () => import("../views/Tim.vue"),
  },
  {
    path: "/karen",
    name: "karen",
    component: () => import("../views/Karen.vue"),
  },
  {
    path: "/meetingRecord",
    name: "meetingRecord",
    component: () => import("../views/MeetingRecord.vue"),
  },
  {
    path: "/kerwin",
    name: "kerwin",
    component: () => import("../views/Kerwin.vue"),
  },
  {
    path: "/homepage",
    name: "homepage",
    component: () => import("../views/Homepage.vue"),
  },
  {
    path: "/login",
    name: "login",
    component: () => import("../views/Login.vue"),
  },
  {
    path: "/questionnaire",
    name: "questionnaire",
    component: () => import("../views/Questionnaire.vue"),
  },
  {
    path: "/register",
    name: "register",
    component: () => import("../views/Register.vue"),
  },
  {
    path: "/personalHomepage",
    name: "personalHomepage",
    component: () => import("../views/PersonalHomepage.vue"),
  },
  {
    path: "/empty",
    name: "empty",
    component: () => import("../views/Empty.vue"),
  },
  {
    path: "/recordCards",
    name: "recordCards",
    component: () => import("../views/RecordCard.vue"),
  },
  {
    path: "/trashBox",
    name: "trashBox",
    component: () => import("../views/TrashBox.vue"),
  },
  {
    path: "/searching",
    name: "searching",
    component: () => import("../views/Searching.vue"),
  }
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
