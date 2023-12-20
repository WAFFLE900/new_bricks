<template>

  <div class="cart_container">
          <div class="additional-textarea">
            <div class="info">
            <h3 class="name">會議記錄</h3>
            <h4 class="date">{{ dateInfo +" "+timeInfo}}</h4>
            <!-- <h4 class="time">15:00~16:00</h4> -->
          </div>
          <div class="split-line" style="width: 100%;"></div>
          <div class="textarea-container">
            <resize-textarea class="textArea" placeholder="請輸入內容" v-model="textValue">{{ content }}</resize-textarea>
            <!-- :maxHeight="150" -->
            <button class="edit_textButton" type="button" @click="edit_textArea"><el-icon><MoreFilled /></el-icon></button>
          </div>
          <!-- <div class="split-line" style="width: 100%;"></div> -->
          <div class="tags">
            <el-tag
              v-for="tag in dynamicTags"
              :key="tag"
              size="large"
              type="danger"
              closable
              :disable-transitions="false"
              @close="handleClose(tag)"
            >
            <span class="tag">{{ tag }}</span>
            </el-tag>
            <el-input
              v-if="inputVisible"
              ref="InputRef"
              v-model="inputValue"
              class="ml-1 w-20"
              size="large"
              type="danger"
              @keyup.enter="handleInputConfirm"
              @blur="handleInputConfirm"
            />
            <el-button
              v-else
              class="button-new-tag ml-1"
              size="large"
              @click="showInput"
            >
            <span class="tag"> + New Tag</span>
            </el-button>
          </div>
        </div>
      </div>
</template>
<script>
import { nextTick, ref } from "vue";
import { ElInput } from "element-plus";

export default {
  name: "DCM",
  setup() {
    const textarea1 = ref("");
    const dateInfo = ref("2023/11/22");
    const timeInfo = ref("15:00~16:00");
    const textValue = ref("請輸入內容請輸入內容請輸入內容請輸入內容請輸入內容請輸入內容請輸入內容請輸入內容請輸入內容請輸入內容請輸入內容請輸入內容請輸入內容請輸入內容請輸入內容請輸入內容請輸入內容請輸入內容請輸入內容請輸入內容請輸入內容請輸入內容請輸入內容請輸入內容請輸入內容請輸入內容請輸入內容請輸入內容請輸入內容請輸入內容請輸入內容請輸入內容請輸入內容請輸入");

    const handleCommand = (command) => {
      inputVisible.value = true;
      // nextTick(() => {
      //   InputRef.value.input.focus();
      // });
    };

    //tags
    const inputValue = ref("");
    const dynamicTags = ref(["Tag1", "Tag2", "Tag3"]);
    const inputVisible = ref(false);
    // const InputRef = ref < InstanceType < typeof ElInput >> new ElInput();
    const handleClose = (tag) => {
      dynamicTags.value.splice(dynamicTags.value.indexOf(tag), 1);
    };
    const showInput = () => {
      inputVisible.value = true;
      // nextTick(() => {
      //   InputRef.value.input.focus();
      // });
    };
    const handleInputConfirm = () => {
      if (inputValue.value) {
        dynamicTags.value.push(inputValue.value);
      }
      inputVisible.value = false;
      inputValue.value = "";
    };

    return {
      textarea1,
      handleCommand,
      inputValue,
      dynamicTags,
      inputVisible,
      // InputRef,
      handleClose,
      showInput,
      handleInputConfirm,
      ElInput,
      dateInfo,
      timeInfo,
      textValue,
    };
  },
};
</script>

<style scoped>
.cart_container {
  display: flex;
  align-items: flex-start;
  width: 890px;
  position: relative;
}
.add_cartButton {
  height: 40px;
  width: 8%;
  margin-top: 0;
  background-color: white;
  border: 1px solid #ccc;
  border-radius: 4px;
}
.cart_container .additional-textarea {
  width: 100%;
  position: relative;
  /* left: 2%; */
  background-color: white;
  border: 1px solid #ccc;
  border-radius: 5px;
  color: var(--base-color-text-el-text-color-primary, #303133);
/* CN regular/body1-Regular */
}
.info {
  display: flex;
  height: 36px;
  position: relative;
}
.name {
  margin-left: 11px;
  margin-top: 8px;
  font-weight: 500;
  position: absolute;
  font-size: 14px;
  color: #606266;
  font-family: PingFang TC;
}
.date {
  display: flex;
  position: absolute;
  right: 16px;
  /* bottom: 12px;  */
  /* margin-right: 16px; */
  margin-top: 5px;
  font-weight: 500;
  color: #606266;
  
  font-size: 14px;
  color: var(--base-color-text-el-text-color-regular, #606266);
/* CN regular/body1-Regular */
/* font-family: PingFang TC; */
font-size: 14px;
font-style: normal;
font-weight: 400;
line-height: 24px;
}
.textarea-container {
  position: relative;
  /* height: ; */
}
.el-input {
  font-size: 14px;
  border: none;
}
.textarea-container .edit_textButton {
  height: 32px;
  width: 45px;
  right: 12px;
  top: 12px;
  background-color: white;
  border: 1px solid #ccc;
  border-radius: 4px;
  position: absolute;
}

.tags {
  display: flex;
  flex-wrap: wrap;
  padding: 8px 16px;
  border: 1px #DCDFE6 solid;
  gap: 4px;
  align-content: center;
  position: relative;
  bottom: -10px;
  left:-10px;
  width:878px;
}
.tag {
  /* margin-right: 4px; */
  width: 68px;
  height: 24px;
  padding: 1px 10px;
}
.ml-1 {
  width: 68px;
  height: 24px;
  padding: 1px 10px;
}

/* .cart_container{
  position: relative;
  display: flex;
} */
  .additional-textarea {
    border-radius: 4px;
    width: 100%;
    padding: 10px;
    border: 1px solid #ccc; /* 大框框的边框样式，你可以根据需要调整颜色和样式 */
  }
  .textarea-container {
    height: auto;
    display: flex;
    align-items: flex-start;
  }
  
  .textArea {
    display: block;
    position: relative;
  
    min-height: 50px;
    font-size: 15px;
    width: 90%;
    border: 0px; /* 移除 textarea 的边框 */
    resize: none; /* 防止調整 textarea 的大小 */
    outline: none; /* 移除点击时的边框 */
    /* border-bottom: 1px #DCDFE6 solid;
    border-top: 1px solid #DCDFE6 ; */

    color: var(--Base-Color-Text---el-text-color-regular, #606266);
    /* CN regular/body1-Regular */
    font-family: PingFang TC;
    font-size: 14px;
    font-style: normal;
    font-weight: 400;
    line-height: 24px; /* 171.429% */
  }
  .split-line {
    border-top: 1px solid #ccc; 
    margin-top: 10px;
    margin-bottom: 10px;
  }

</style>
