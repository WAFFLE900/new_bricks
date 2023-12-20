<template>
    <div class="karen">
  
      <div class="button-container">
        <el-backtop visibility-height="0" class="backtop">
                <div id="backtop">
                    <el-icon class="icon"><upload/></el-icon>
                </div>
                </el-backtop>
            
            <el-button type="button" @click="showBasicInfo"><el-icon><Edit /></el-icon>會議基本資訊</el-button>
            <el-button :plain="true" @click="copyLinkBtn"><el-icon><Link /></el-icon></el-button>
      </div>
      <div class="form-container">
        
        <table class="form-table">
          <tr>
            <td class="left-bar">
              <label for="meetingName">會議名稱</label>
            </td>
            <td class="input-cell">
              <input type="text" id="meetingName" v-model="meetingName" class="text-input" :placeholder="placeholder" @focus="clearPlaceholder" @blur="restorePlaceholder">
            </td>
          </tr>
          <tr>
            <td class="left-bar">
              <label for="time">時間</label>
            </td>
            <td class="input-cell">
              <input type="place" id="time" v-model="time" class="text-input" placeholder="-">
            </td>
          </tr>
          <tr>
            <td class="left-bar">
              <label for="attend">出席人員</label>
            </td>
            <td class="input-cell">
              <el-tag class="ml-2" type="danger" v-for="(option, index) in optionsA" :key="index">{{ option.label }}</el-tag>
              <!-- <input type="attend" id="attend" v-model="attends" class="text-input" placeholder="-"> -->
            </td>
          </tr>
          <tr>
            <td class="left-bar">
              <label for="place">地點</label>
            </td>
            <td class="input-cell">
              <input type="place" id="place" v-model="place" class="text-input" placeholder="-">
            </td>
          </tr>
          <tr>
            <td class="left-bar">
              <label for="absent">缺席人員</label>
            </td>
            <td class="input-cell">
              <el-tag class="ml-2" type="danger" v-for="(option, index) in optionsB" :key="index">{{ option.label }}</el-tag>

              <!-- <input type="absent" id="absent" v-model="absents" class="text-input" placeholder="-"> -->
            </td>
          </tr>
          <tr>
            <td class="left-bar">
              <label for="record">紀錄人員</label>
            </td>
            <td class="input-cell">
              <el-tag class="ml-2" type="danger" v-for="(option, index) in optionsC" :key="index">{{ option.label }}</el-tag>
              <!-- <input type="record" id="record" v-model="recorder" class="text-input" placeholder="-"> -->
            </td>
          </tr>
        </table>
      </div>
      
      <div class="overlay" v-show="showOverlay"></div>
      <div class="form" v-show="form.show">
          <p class="formName">設定會議基本資訊
              <button class="close-button" type="button" @click="close"><el-icon><Close /></el-icon></button>
          </p>
          <el-form :model="form" >
              <el-form-item label="會議名稱">
              <el-input v-model="form.data.formName"  :style="{ width: '500px' }" placeholder="輸入會議名稱"/>
          </el-form-item>
        <el-form-item label="日期">
          <div class="demo-date-picker" >
          <el-date-picker
              v-model="form.data.date"
              type="date"
              placeholder="Pick a date"
              :default-value="new Date()"
              :style="{ width: '500px' }"
              
          />
          </div>
        </el-form-item>
        <el-form-item label="開會時間">
            <div class="demo-range" >
              <el-time-picker
              v-model="form.data.time"
              is-range
              range-separator="To"
              start-placeholder="Start time"
              end-placeholder="End time"
              :default-value="[new Date(), new Date()]"
              />
              </div>
          </el-form-item>
          <el-form-item label="出席人員">
          <el-select
              v-model="valueA"
              multiple
              filterable
              allow-create
              default-first-option
              :reserve-keyword="true"
              placeholder="選擇出席人員"
              :style="{ width: '500px' }"
              @change="handleSelectChangeA"
          >
      <el-option
        v-for="item in optionsA"
        :key="item.value"
        :label="item.label"
        :value="item.value"
      />
    </el-select>
        </el-form-item>
        <el-form-item label="會議進行地點">
              <el-input v-model="form.data.place"  :style="{ width: '500px' }" placeholder="輸入會議地點"/>
          </el-form-item>
          <el-form-item label="缺席人員">
            <el-select
            v-model="valueB"
            multiple
            filterable
            allow-create
            default-first-option
            :reserve-keyword="false"
            placeholder="選擇缺席人員"
            :style="{ width: '500px' }"
            @change="handleSelectChangeB"
          >
      <el-option
        v-for="item in optionsB"
        :key="item.value"
        :label="item.label"
        :value="item.value"
      />
    </el-select>
        </el-form-item>
        <el-form-item label="紀錄負責人員">
          <el-select
      v-model="valueC"
      multiple
      filterable
      allow-create
      default-first-option
      :reserve-keyword="false"
      placeholder="選擇會議記錄人員"
      :style="{ width: '500px' }"
      @change="handleSelectChangeC"
    >
      <el-option
        v-for="item in optionsC"
        :key="item.value"
        :label="item.label"
        :value="item.value"
      />
    </el-select>
        </el-form-item>
        
        <el-form-item>
          <el-button class="commit_button"  @click="onSubmit" >
            <el-icon><DocumentChecked /></el-icon>  <span style="margin-left: 8px;">儲存</span>
          </el-button>
        </el-form-item>
      </el-form>
      </div>
      <!-- <BasicInfo /> -->
      <!-- <Delete /> -->

    </div>
  </template>
  
  <script >
  
  import axios from 'axios';
  import { ref } from 'vue';
  import { ElNotification, useTransitionFallthroughEmits } from 'element-plus';
  import { ElMessage } from 'element-plus';
  export default {
    components: {
      // LinkCopy,
      // Delete,
      // BasicInfo,
    },
    
    data() {
      return {
        form: {
          show: false,
          data: {
            formName: '',
            date:'',
            time:'',
            place:'',
            // 其他表單項目
          },
      },
      meetingName: '',
      time:'',
      attends:[],
      place:'',
      absents:'',
      recorder:'',
        
        formPlace:'',
        
        showOverlay: false,
        value: '',
        placeholder: "輸入會議名稱",

        // height: '30px',
        // basicComponent: null,
        // date: '',
        // value2: [
        //   new Date(2016, 9, 10, 8, 40),
        //   new Date(2016, 9, 10, 9, 40),
        // ],

        // height: '30px',
        // basicComponent: null,
        // value1: '',
        // value2: [
        //   new Date(), 
        //   new Date(),
        // ],

        valueA: [],
        optionsA: [],
        valueB: [],
        optionsB: [],
        valueC: [],
        optionsC: [
          // { value: 'c', label: 'c' }
        ],
  
      };
    },
    methods: {
      clearPlaceholder() {
        this.placeholder = "";
      },
      restorePlaceholder() {
        if (!this.meetingName) {
        this.placeholder = "輸入會議名稱";
        }
      },
      recover() {
        ElNotification({
          dangerouslyUseHTMLString: true,
          title: '成功復原會議記錄',
          message: '<a href="/path/to/recovery/file" style="color: #67C23A; text-decoration: underline;">點擊檢視復原檔案</a>',
          type: 'success',
          position: 'bottom-right',
        });
        },
        
      copyLinkBtn() {
        ElMessage({
          message: '會議記錄連結已複製',
          type: 'success',
          position: 'bottom-right',
        });
      },
      deleteForever(){
        ElMessage('您已永久刪除會議記錄')
      }, 
      deleteRecord(){
        ElMessage.error('您已刪除會議記錄');
      },
      showBasicInfo(){
        this.showOverlay = true;
        this.form.show = true;
      },
  
      close(){
        this.showOverlay = false;
        this.form.show = false;
      },
      handleSelectChangeA(selectedValues) {
        this.handleSelectChange(selectedValues, this.optionsA, this.valueA);
      },
      handleSelectChangeB(selectedValues) {
        this.handleSelectChange(selectedValues, this.optionsB, this.valueB);
      },
      handleSelectChangeC(selectedValues) {
        this.handleSelectChange(selectedValues, this.optionsC, this.valueC);
      },
      handleSelectChange(selectedValues, options, value,who) {
        selectedValues.forEach((selectedValue) => {
          const existsInOptions = options.some((option) => option.value === selectedValue);
  
          if (!existsInOptions) {
            options.push({
              value: selectedValue,
              label: selectedValue,
            });
          }
  
          const existsInValue = value.includes(selectedValue);
  
          if (!existsInValue) {
            value.push(selectedValue);
          }
          
        });
      },
      onSubmit() {
        const selectedDate = this.form.data.date;
        const selectedTimeRange = this.form.data.time; // 獲取選擇的時間範圍

        // 格式化開始時間的小時和分鐘
        const startHours = ('0' + selectedTimeRange[0].getHours()).slice(-2);
        const startMinutes = ('0' + selectedTimeRange[0].getMinutes()).slice(-2);

        // 格式化結束時間的小時和分鐘
        const endHours = ('0' + selectedTimeRange[1].getHours()).slice(-2);
        const endMinutes = ('0' + selectedTimeRange[1].getMinutes()).slice(-2);
        //開始加結束
        const meetingTime = `${startHours}:${startMinutes} - ${endHours}:${endMinutes}`;


        this.meetingName = this.form.data.formName;
        this.time =new Date(selectedDate).toISOString().split('T')[0]+" "+ meetingTime;

        this.place = this.form.data.place;
        // this.attends = this.optionsA.map(option => option.label);
        


        ElMessage({
          message: '已儲存會議基本資訊',
          type: 'success',
        });
        this.showOverlay = false;
        this.form.show = false;
      },
      
    },
  
  };
  // const date = ref<[Date, Date]>([
  //   new Date(2016, 9, 10, 8, 40),
  //   new Date(2016, 9, 10, 9, 40),
  // ])
  </script>
  
  <style scoped>
  .demo-range .el-date-editor {
    width: 100%;
    
  }

  /* .karen{
    position: relative;
  } */
  
  .form-container {
    border-radius: 4px;
    /* position: absolute; */
    display: flex;
    flex-direction: row;
    gap: 14px;
    width: 910px;
    border-collapse: collapse;
  }
  
  .left-bar {
    padding: 12px;
    padding-left: 16px;
    width: 73px;
    text-align: left;
    font-size: 15px;
    
    border: 1px solid #ccc;
    background-color: #EBEEF5; /* 添加背景顏色 */
  }
  
  .input-cell {
    padding: 8px;
    border: 1px solid #ccc;
    width: 837px;
  }
  
  .text-input {
    width: 100%;
    border: none;
    outline: none;
    /* -webkit-appearance: none; */
    font-size: 14px;
  }
  
  
  .button-container {
      /* position: absolute; */
      display: flex;
      height:40px;
      width:910px;
      margin-bottom: 14px;
      margin-left: 696px;
      /* top: 20px;
      left: 248px; */
      /* margin-bottom: 0px; */
  }
   /* .button-container button:first-child {
     margin-left: 400px;
      width: 50px;
      background-color: white;
      border: 1px solid #ccc;
      border-radius: 4px;
  } */
  /* .button-container button:nth-child(2) {
    margin-right: 20px;
    width: 140px;
    background-color: white;
    border: 1px solid #ccc;
    border-radius: 4px;
    display: flex;
    align-items: center;
    
  }  */
  .button-container button:nth-child(2) .el-icon {
    margin: 10px; /* 设置图标与文本之间的右边距 */
  }
  .button-container button:nth-child(3) {
    margin-right: 0px; 
    width: 50px;
    background-color: white;
    border: 1px solid #ccc;
    border-radius: 4px;
  }
  .cart_container {
    margin-left: 383px;
    display: flex;
    align-items: flex-start;
  }
  .formName {
      display: flex;
    justify-content: space-between;
    /* 第一个子元素在容器的起始位置，最后一个子元素在容器的末尾位置 */
    align-items: center;
    font-size: 20px;
    text-align: left;
    font-weight: bold;
    width: 500px;
  }
  
  button.close-button {
    border: none;
    background: none;
   margin-left: 290px;
   outline: none;  
    font-size: 1em;
    cursor: pointer;
  }
  p {
    margin-top: 0;
    margin-bottom: 15px;
  }
  
  .overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background: rgba(0, 0, 0, 0.5); /* 半透明黑色 */
    z-index: 9; /* 放在最上层 */
   
  }
  .form{
      width: 500px;
      position: absolute;
      top: -40px;
      left:300px;
      z-index: 10;
      border: 1px solid #ccc;
      padding: 20px;
      border-radius: 4px;
      background-color: #ffffff;
  }
  .form .el-form-item {
    /* margin-bottom: 25px; */
    display: flex; /* 使用 Flexbox 布局 */
    flex-direction: column; /* 垂直方向布局 */
    align-items: flex-start; /* 靠左对齐 */
  }
  
  /* input內的字 */
  .el-input {
    font-size: 15px;
  }
  .demo-range .el-form-item .el-time-picker {
    width: 100%;
  }
  
  
  .commit_button{
      margin-left:418px;
      background: #EB2348;
      border: 1px solid #EB2348;
      display: flex;
      color: #ffffff;
      justify-content: flex-end; /* 将内容靠右对齐 */
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
 .input-cell {
  text-align: left;
}
.el-tag {
  margin-left: 5px;
}

  </style>