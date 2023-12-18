<template>
  <div class="tim">
    <h1>This is Tim's page</h1>
    <el-button round @click="showBtn">show the button</el-button>
    <div v-show="isShow">
      <el-button type="primary" round @click="goToCalender">calender</el-button>
      <el-popover
        placement="top-start"
        title="Hello"
        :width="200"
        trigger="hover"
        content="這個我們專案應該會用到"
      >
        <template #reference>
          <el-button class="m-2">Hover to activate</el-button>
        </template>
      </el-popover>
      <el-button type="info" round>Info</el-button>
      <el-button @click="showAlert" type="warning" round>Warning</el-button>
      <!-- <Survey msg="Welcome to Tim's page" /> -->
    </div>

    <Survey />
  </div>
</template>

<script>
import { ref } from "vue";
// @ is an alias to /src
import Survey from "@/components/TimBricks/Survey.vue";
import { useRouter } from "vue-router";

export default {
  name: "Tim",
  components: {
    Survey,
  },
  setup() {
    const router = useRouter();
    const isShow = ref(false);
    const showBtn = () => {
      isShow.value = !isShow.value;
    };
    const showAlert = () => {
      console.log("warning");
      window.alert("這是一個警告！");
    };
    const goToCalender = () => {
      // 在這裡導航到另一個介面
      router.push({ name: "calender" });
    };
    return {
      isShow,
      showBtn,
      showAlert,
      goToCalender,
    };
  },
};
</script>
