<template>
  <el-calendar v-model="value" />
</template>

<script>
import { ref } from "vue";
export default {
  name: "Calender",
  setup() {
    const value = ref(new Date());
    return {
      value,
    };
  },
};
</script>
