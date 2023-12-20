<template>
  <div id="background">
    <div id="center">
      <el-empty :image-size="200" description="點選新增建立新的會議紀錄" :root =--el-empty-fill-color-0>
        <el-button id="addBtn" @click="addClicked">
          <div id="buttonContent">
            <el-icon><circle-plus/></el-icon>新增
          </div></el-button>
      </el-empty>
    </div>
  </div>
</template>

<script>
export default {
  setup(props,{emit}){
    const addClicked = () => {
      emit('showAdd',true);
    };

    return{
      addClicked,
    };
  }
}
</script>

<style>
    #background{
        background-color: #F2F3F5;
        /* width: auto; */
        /* height: auto;     */
        /* flex-shrink: 1; */
        position: absolute;
        display: block;
        align-items: center; /* 在交叉轴上垂直居中 */
        justify-content: center;
    }
    #center{
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 20px;
      position: absolute;
      left: 0;

    }


    #center #buttonContent {
      display: flex;
      height: 32px;
      min-height: 24px;
      max-height: 40px; 
      justify-content: center;
      align-items: center;
      gap: 8px;

      color: #FFF;
      font-size: 13px;
      font-weight: 400;
      line-height: 22px; /* 169.231% */
    }

    #center #addBtn{
      border-radius: 2px;
      background: #C91F2F;
      padding: 4px 16px;
    }

    /* #empty{
      --el-empty-fill-color-1
    } */
</style>