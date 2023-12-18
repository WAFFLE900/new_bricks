<template>
  <div class="sharon" @contextmenu.prevent>
    <!-- @update="selectedItemUpdate" -->
    <!-- :activeIndex="currentActive" -->
    <!-- @showAdd="show" -->
      <side-bar class="sideBar"  ></side-bar>
      <nav-bar-main class="navBar"></nav-bar-main>

    <!-- 新增、會議記錄主頁 -->
    <!-- v-show="isShowed" -->
    <div class="navAndCont"  id="new" v-if="showedInfo">
      <div :class="meetingClass">
        <div class="info"><meeting ></meeting></div>
        <div class="textBlock">
          <text-block v-for="cart in quantity" :key="cart" @add_cart="add_block"/>
      </div>
        
      </div>
    </div>

      <div class="result" v-else>    
            <el-backtop visibility-height="0" class="backtop">
            <div id="backtop">
                <el-icon class="icon"><upload/></el-icon>
            </div>
            </el-backtop>
            <div class="toolBar">
            <ordering/>
            <sort/>
        </div>
            <!-- <text-block v-for="item in 10" :key="item"/> -->
            <document-with-info v-for="item in 10" :key="item"/>
      </div>

      <!-- 標籤 -->
      <div trigger="click" class="tagsPlace" @click="showTags">
        <span class="el-dropdown-link">
          標籤<el-icon class="el-icon--right"><arrow-down /></el-icon>
        </span>
      </div>
      <tag-search-area v-show="tagShowed" class="tagInside" @showBlock="showInfo"></tag-search-area>
      
  </div>
</template>


<script>
import { ref } from "vue";
// import axios from "axios";
import SideBar from "../components/SideBar.vue";
import NavBarMain from '../components/NavBarMain.vue';
import meeting from '../components/meeting.vue';
import TextBlock from "@/components/TextBlock.vue";
import TagSearchArea from '../components/KerwinBricks/TagSearchArea.vue';
import { useRouter } from "vue-router";
import Ordering from '../components/SharonBricks/Ordering.vue';
import sort from '../components/SharonBricks/Sort.vue';
import DocumentWithInfo from "@/components/KerwinBricks/DCMwithDate.vue";


export default {
  components: {
    SideBar,
    NavBarMain,
    meeting,
    TextBlock,
    TagSearchArea,
    sort,
    Ordering,
    DocumentWithInfo

  },
  setup(props,{emit}) {
    const meetingClass = ref("meeting");
    const activeOption = ref(null);  
    const isShowed = ref(false);  
    const tagShowed = ref(false);
    const router = useRouter();
    const currentActive = ref("1-1");
    const showedInfo = ref(true);
    const quantity = ref(1);

    const showTags = () =>{
      tagShowed.value = !tagShowed.value;
      if(tagShowed.value === true){
        meetingClass.value = "showingClass";
      }
      else{
        meetingClass.value = "meeting";
      }
    }

    const showInfo = (value) =>{
      showedInfo.value = value;
    };
    const add_block = () =>{
      quantity.value +=1;
    }

    return {
      activeOption,
      // selectedItemUpdate,
      isShowed,
      // StopShowing,
      // show,
      showTags,
      tagShowed,
      meetingClass,
      // nextPage,
      currentActive,
      showInfo,
      showedInfo,
      quantity,
      add_block,
    };
  },
};
</script>

<style scoped>
 .sharon{
    position: relative;
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
 .navAndCont{
  background-color: #DCDFE6;
  position: absolute;
  left: 200px;
  width:auto;
  top: 0;
  right: 0;
 }
 .info{
  position: absolute;
 }

 .textBlock{
  position: absolute;
  
  top: 350px;
  left: -65px;
  display: grid;
  grid-row-gap: 8px;
  /* gap: 8px; */
 }

 .meeting{
  position: absolute;
  top: 68px;
  left:248px;
  
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

 .tagMenu{
  width: 372px;
 }

 .showingClass{
  position: absolute;
  top: 68px;
  /* right: 430px; */
  left: 66px;
 }

 .result{
    position: absolute;
    display:grid;
    /* flex-direction: row; */
    /* flex-wrap: wrap; */
    row-gap: 8px;
    top: 68px;
    /* margin-top: 128px; */
    /* width: 572px; */
    left:246px;
 }

 .backtop{
    
 }

 #backtop{
    background-color: var(--el-bg-color-overlay);
    box-shadow: var(--el-box-shadow-lighter);
    text-align: center;
    color: #C91F2F;
    padding: 9px 16px;
    justify-content: left;
    position: fixed;
    left: 255px;
    top: 70px;
 }

 .icon{
    font-size: 14px;
 }

 .toolBar{
    display:flex;
    gap: 12px;
    /* position: absolute; */
    top: 68px;
    /* right:0; */
    margin-bottom: 12px;
    justify-content: right;
    text-align: right;
    width: 1fr;
    /* background: #F2F3F5; */
    /* left: 46px; */
    /* right: 700px; */
 }

</style>
