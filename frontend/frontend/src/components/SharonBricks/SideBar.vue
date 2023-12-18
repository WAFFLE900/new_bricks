<template>
  <div id="sidebar">
    <div id="container">
    <div id="title" @click="menu_clicked">
      <el-icon id="logo" :color = "incolor"><elementPlus /></el-icon>
      <p id="title-name">{{ project_name }}</p>
    </div>
    <div id="btnBlock">
      <el-button id="addBtn" @click="addClicked">新增</el-button>
    </div>
    
    <!-- 選單部分 -->
    <div id="menuBar">  
      <el-row class="tac">
      <el-col :span="24">
        <!-- :active-color = incolor -->
      <el-menu
        unique-opened = true
        class="el-menu-vertical-demo"
        :active-text-color = incolor
        @select="selectedItem"
        @open="handleOpen"
        @close="handleClose"
        :active-bg-color= active_color
      >
        <el-sub-menu index="1" class="menu">
          <template #title>
            <el-icon><list /></el-icon>
            <span>會議記錄</span>
          </template>
            <el-menu-item index="1-1">全部</el-menu-item>
            <el-menu-item index="1-2">垃圾桶</el-menu-item>
            <!-- @click="goTrashBox" -->
        </el-sub-menu>
        <el-sub-menu index="2" class="menu">
        <template #title>
            <el-icon><opportunity /></el-icon>
            <span>提案區</span>
          </template>
            <el-menu-item index="2-1">全部</el-menu-item>
            <el-menu-item index="2-2">垃圾桶</el-menu-item>        
        </el-sub-menu>
        <el-sub-menu index="3" class="menu">
          <template #title>
            <el-icon><span class="material-icons">&#xE4FD;</span></el-icon>
            <span>組織架構圖</span>
          </template>
            <el-menu-item index="3-1">全部</el-menu-item>
            <el-menu-item index="3-2">垃圾桶</el-menu-item>
        </el-sub-menu>
      </el-menu>
    </el-col>
  </el-row>

  </div> <!-- menuBar -->
  </div> <!-- container -->
</div>
  
</template> 

<script>
import { ref } from 'vue';

export default {
  components: {
    
  },
  setup(props,{emit}) {
    const active_color = ref("#fff")
    const project_name = "專案名稱";
    const incolor = "#C91F2F";
    const activeOption = ref(null);
    const isClicked = ref(false);

    // 按下後字體改變顏色
    const menu_clicked = () =>{
      active_color.value = "#FAE4E7";
    };

    // 提供父元件選擇的改變
    const selectedItem = (index) =>{
      activeOption.value = index;
      emit('update',index);
    };

    // 提供父元件點擊事件
    const addClicked = (value) =>{
      value = true;
      emit('showAdd',value);
    };

    // 改變頁面時停止顯示
    // const stopShowing = () =>{
    //   isClicked.value = false;
    //   // emit('stop', isClicked.value);
    // };

    return {
      project_name,
      incolor,
      active_color,
      menu_clicked,
      selectedItem,
      activeOption,
      // router,
      addClicked,
      // stopShowing,
      isClicked,

    };
  }
}
</script>



<style scoped>
  #sidebar{
    z-index: 10;
    display: flex;
    width: 200px;
    height: 100vh;
    flex-direction: column;
    justify-content: center;
    /* align-items: center; */
    vertical-align: top;
    flex-shrink: 0;
    position: fixed;
    /* top: 0;
    left: 0; */
    border-right: 1px solid  #E4E7ED;
    background: #FFF;
    box-shadow: 0px 0px 12px 0px rgba(0, 0, 0, 0.12);
  }
  #container{
    position: inherit;
    top: 0;
  }

  #title{
    display: flex;
    width: 100%;
    padding: 0px 16px;
    justify-content: left;
    align-items: center;
    height: 48px;
    position: relative;
    top: 0;
    left: 0px;
    /* padding-left: 16px; */
  }

  

  #title #logo{
    display: block;
    width: auto;
    height: auto;
    padding: 4px;
  }

  #title #title-name{
    color: #303133;
  /* CN bold/Headline3-Bold */
    font-size: 16px;
    font-style: normal;
    font-weight: 600;
    line-height: 24px; /* 150% */
    z-index: 10;
  }

  #addBtn{
    display: flex;
    width: 168px;
    min-height: 24px;
    max-height: 40px;
    padding: 20px 16px;
    justify-content: center;
    align-items: center;
    gap: var(--space-size-small, 8px);
    flex: 1 0 0;

    border-radius: 999px;
    color:#FFF;
    background: #C91F2F;
    position: relative;
    top: 0;
    
    font-size: 14px;
    font-style: normal;
    font-weight: 400;
    line-height: 32px;
  }

  #btnBlock{
    padding: 12px;
    position: relative;
    top:0;
  }

  .el-menu-vertical{

  }

  #menuBar{
    font-size: 14px;
    font-style: normal;
    font-weight: 400;
    line-height: 24px;
  }

  #menuBar .menu{
    color: #C91F2F;
  }

  .menu :active{
    
  }



  
</style>