<template>
    <side-bar class="sideBar"/>
    <div class="navAndCont" id="empty">
      <nav-bar class="navBar"></nav-bar>
      <empty-back class="content" @showAdd="show"></empty-back>
      <!-- 標籤 -->
      <div trigger="click" class="tagsPlace" @click="showTags">
        <span class="el-dropdown-link">
          標籤<el-icon class="el-icon--right"><arrow-down /></el-icon>
        </span>
      </div>
      <tag-search-area v-show="tagShowed" class="tagInside"></tag-search-area>
    </div >
  
</template>

<script>
import SideBar from '../components/SideBar.vue'
import EmptyBack from '@/components/EmptyBack.vue';
import NavBar from '@/components/NavBar.vue';
import TagSearchArea from '@/components/KerwinBricks/TagSearchArea.vue';
export default {
    name: 'empty',
    components: {
        SideBar,
        EmptyBack,
        NavBar,
        TagSearchArea,
    },
    setup(){
        return{

        };
    }

}
</script>

<style scoped>
.navAndCont{
  background-color: #DCDFE6;
  position: absolute;
  left: 200px;
  width:auto;
  top: 0;
  right: 0;
 }

 .tagsPlace{
  position: absolute;
  right: 32px;
  top: 68px;
  border-radius: var(--radius-button-large-radius, 4px);
  border: 1px solid var(--base-color-border-el-border-color, #DCDFE6);
  background: #FFF;
  padding: 4px 16px;
 }

 .el-dropdown-link{
  display: flex;
  gap: 8px;
  cursor: pointer;
 }

 .el-dropdown-link{
  color: #C91F2F;
 }

 .tagInside{
  position: absolute;
  right: 32px;
  top: 114px;
  z-index: 10;
 }

 .navBar{
    position: absolute;
    top: 0;
    left: 200px;
    right: 0;
    /* grid-area: navBar; */
 }
 .sideBar{
    /* grid-area: sideBar; */
    position: absolute;
    top: 0;
    left: 0;
    bottom: 0;
 }
 .content{
    /* grid-area: content; */
    position: fixed;
    left: 600px;
    /* right: 0; */
    top: 30vh;
    bottom: 0;
 }

</style>