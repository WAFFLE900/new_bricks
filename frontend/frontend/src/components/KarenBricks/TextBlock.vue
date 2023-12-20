<template>
    
  <div class="cart_container">
        <button class="add_cartButton" type="button" @click="add_cart"><el-icon><Plus /></el-icon></button>
        <div class="additional-textarea">
          <div class="textarea-container">
            <resize-textarea class="textArea" placeholder="請輸入內容" v-model="textValue"></resize-textarea>
            <button class="edit_textButton" type="button" @click="edit_textArea"><el-icon><MoreFilled /></el-icon></button>
          </div>
          <div class="split-line" style="width: 100%;"></div>
          <textarea id="tag" v-model="tag" placeholder="選擇標籤類型並建立標籤" style="height: 20px; "></textarea> 
        </div>
      </div>
</template>

<script>
export default {
    setup(){

        return{

        };
    }
}
</script>

<style scoped>
    .cart_container{
        position: relative;
        display: flex;
    }
    .additional-textarea {
    border-radius: 4px;
    width: 890px;
    padding: 10px;
    border: 1px solid #ccc; /* 大框框的边框样式，你可以根据需要调整颜色和样式 */
  }
  .textarea-container {
    height: auto;
    display: flex;
    align-items: flex-start;
  }
  
  .textArea {
    
    min-height: 50px;
    font-size: 15px;
    width: 100%;
    border: 0px; /* 移除 textarea 的边框 */
    resize: none; /* 防止調整 textarea 的大小 */
    outline: none; /* 移除点击时的边框 */
  }
  #tag{
    font-size: 15px;
    width: 100%;
    border: 0px; /* 移除 textarea 的边框 */
    resize: none; /* 防止調整 textarea 的大小 */
    outline: none;
  }
  .split-line {
    border-top: 1px solid #ccc; 
    margin-top: 10px;
    margin-bottom: 10px;
  }

  .add_cartButton{
    height: 40px;
    width: 50px;
    margin-right: 15px;
    background-color: white;
    border: 1px solid #ccc;
    border-radius: 4px;
  }
  .edit_textButton{
    height: 35px;
    width: 50px;
    margin-left: 0px;
    background-color: white;
    border: 1px solid #ccc;
    border-radius: 4px;
  }
</style>