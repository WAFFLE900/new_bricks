<template>
    <div class="form" v-show="form">
        <p class="formName">設定會議基本資訊
            <button class="close-button" type="button" @click="close"><el-icon><Close /></el-icon></button>
        </p>
        <el-form :model="form" >
            <el-form-item label="會議名稱">
            <el-input v-model="form.name"  :style="{ width: '500px' }" placeholder="輸入會議名稱"/>
        </el-form-item>
      <el-form-item label="日期">
        <div class="demo-date-picker" >
        <el-date-picker
            v-model="value1"
            type="date"
            placeholder="Pick a date"
            :default-value="new Date(2010, 9, 1)"
            :style="{ width: '500px' }"
        />
        </div>
      </el-form-item>
      <el-form-item label="開會時間">
          <div class="demo-range"  :style="{ width: '440px' }">
            <el-time-picker
            v-model="value2"
            is-range
            range-separator="To"
            start-placeholder="Start time"
            end-placeholder="End time"
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
            <el-input v-model="form.place"  :style="{ width: '500px' }" placeholder="輸入會議地點"/>
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
  </template>
  
  <script setup>
  import { reactive } from 'vue'
  import { ref } from 'vue'

  const value1 = ref('')
  const value2 = ref<[Date, Date]>([
      new Date(2016, 9, 10, 8, 40),
      new Date(2016, 9, 10, 9, 40),
  ])
  
  const valueA = ref([]);
  const optionsA = ref([
    {
      value: 'HTML',
      label: 'HTML',
    }
  ]);
  const handleSelectChangeA = (selectedValues) => {
    selectedValues.forEach((selectedValue) => {
      const existsInOptions = optionsA.value.some((option) => option.value === selectedValue);
      
      if (!existsInOptions) {
        optionsA.value.push({
          value: selectedValue,
          label: selectedValue,
        });
      }
      // 检查值是否已存在于 valueA 中
      const existsInValue = valueA.value.includes(selectedValue);
      
      if (!existsInValue) {
        valueA.value.push(selectedValue);
      }
    });
  };
  const valueB = ref([]);
    const optionsB = ref([
      {
        value: 'w',
        label: 'w',
      }
    ]);
    const handleSelectChangeB = (selectedValues) => {
    selectedValues.forEach((selectedValue) => {
      const existsInOptions = optionsB.value.some((option) => option.value === selectedValue);
      
      if (!existsInOptions) {
        optionsB.value.push({
          value: selectedValue,
          label: selectedValue,
        });
      }
      // 检查值是否已存在于 valueB 中
      const existsInValue = valueB.value.includes(selectedValue);
    
      if (!existsInValue) {
        valueB.value.push(selectedValue);
      }
    });
  };
  const valueC = ref([]);
    const optionsC = ref([
      {
        value: 'c',
        label: 'c',
      }
    ]);
    const handleSelectChangeC = (selectedValues) => {
    selectedValues.forEach((selectedValue) => {
      const existsInOptions = optionsC.value.some((option) => option.value === selectedValue);
      
      if (!existsInOptions) {
        optionsC.value.push({
          value: selectedValue,
          label: selectedValue,
        });
      }
      // 检查值是否已存在于 valueC 中
      const existsInValue = valueC.value.includes(selectedValue);
    
      if (!existsInValue) {
        valueC.value.push(selectedValue);
      }
    });
  };
  // do not use same name with ref
  const form = reactive({
   
    name: '',
    region: '',
    delivery: false,
    type: [],
    resource: '',
    desc: '',
    place:'',
  })
 
  const onSubmit = () => {
    console.log('submit!')
  }
  </script>
<style scoped>
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
 /* margin-left: 290px; */
 outline: none;  
  font-size: 1em;
}
p {
  margin-top: 0;
  margin-bottom: 15px;
}
.form{
    width: 500px;
    /* margin-left: 200px; */
    /* margin-bottom: 300px; */
    border: 1px solid #ccc;
    padding: 20px;
    border-radius: 4px;
    position: absolute;
    z-index: 1000;
    background-color: #ffffff;
}
.form .el-form-item {
  margin-bottom: 25px;
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


</style>