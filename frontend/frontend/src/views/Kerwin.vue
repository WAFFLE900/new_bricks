<template>
  <div class="kerwin">
    <TagSearchArea />
    <div style="margin: 20px"></div>
    <documentArea />
    <div style="margin: 20px"></div>
    <documentAreaWithInfo />
  </div>
</template>

<script>
import TagSearchArea from "@/components/KerwinBricks/TagSearchArea.vue";
import documentArea from "@/components/KerwinBricks/DCM.vue";
import documentAreaWithInfo from "@/components/KerwinBricks/DCMwithDate.vue";
export default {
  name: "Kerwin",
  components: { TagSearchArea, documentArea, documentAreaWithInfo },
};
</script>

<style scoped>
.kerwin {
  background-color: #ccc;
  height: 200vh;
  width: 100%;
  /* margin: 2rem; */
  /* padding: 2rem; */
}
</style>
