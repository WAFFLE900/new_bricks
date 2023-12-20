<template>
  <div class="tagSearchArea">
    <div class="tagTypingArea">
      <!-- <el-button class="taglist">標籤</el-button> -->
      <el-select
        v-model= "selectedOptions"
        filterable
        :options="options1"
        placeholder="點擊選擇或輸入標籤"
        multiple = "true"
        autocomplete="false"
        automatic-dropdown="false"
        @remove-tag="deleteTag"
      >
      </el-select>
      
    </div>
    <div class="trans"></div>
    <div class="demo-collapse">
      <el-collapse v-model="activeNames" @change="handleChange">
        <el-collapse-item name="1">
          <template #title><span>
            日期</span>
            <el-icon class="header-icon">
              <info-filled />
            </el-icon>
          </template>
          <div class="order scrollbar">
            <el-check-tag
              v-for="(tagD, idx) in tagsDate"
              :key="`tagD_${idx}`"
              :checked="tagD.checked"
              @change="onChange('tagD', idx)"
              :class="{ tagChecked: tagD.checked, tagUnchecked: !tagD.checked }"
            >
              {{ tagD.label }}
            </el-check-tag>
            <p class="no-use">
              Lorem ipsum dolor sit amet consectetur adipisicing elit. Dolor
              sequi harum deserunt eum eius aliquid temporibus velit quos.
              Recusandae commodi tenetur blanditiis omnis voluptates nesciunt
              dolores voluptas quam praesentium quia odit, veritatis modi
              consequuntur, amet atque iure rerum, quos accusantium cupiditate
              ad harum dignissimos! Dolores a neque pariatur atque incidunt
              quaerat culpa veniam quas officiis sequi sed vitae quod commodi,
              eveniet nobis officia consectetur aut, ab optio similique, placeat
              aspernatur. Laborum soluta minima expedita. Harum incidunt culpa
              porro, praesentium nulla ut blanditiis eaque iusto officia itaque
              reiciendis adipisci et aliquid facilis ipsa explicabo nam sequi ad
              laborum qui illum corporis.
            </p>
          </div>
        </el-collapse-item>
        <el-collapse-item title="事項" name="2">
          <div class="order scrollbar">
            <el-check-tag
              v-for="(tag2, idx) in tagsThing"
              :key="`tag2_${idx}`"
              :checked="tag2.checked"
              @change="onChange('tag2', idx)"
              :class="{ tagChecked: tag2.checked, tagUnchecked: !tag2.checked }"
            >
              {{ tag2.label }}
            </el-check-tag>
            <p class="no-use">
              Lorem ipsum dolor sit amet consectetur adipisicing elit. Dolor
              sequi harum deserunt eum eius aliquid temporibus velit quos.
              Recusandae commodi tenetur blanditiis omnis voluptates nesciunt
              dolores voluptas quam praesentium quia odit, veritatis modi
              consequuntur, amet atque iure rerum, quos accusantium cupiditate
              ad harum dignissimos! Dolores a neque pariatur atque incidunt
              quaerat culpa veniam quas officiis sequi sed vitae quod commodi,
              eveniet nobis officia consectetur aut, ab optio similique, placeat
              aspernatur. Laborum soluta minima expedita. Harum incidunt culpa
              porro, praesentium nulla ut blanditiis eaque iusto officia itaque
              reiciendis adipisci et aliquid facilis ipsa explicabo nam sequi ad
              laborum qui illum corporis.
            </p>
          </div>
        </el-collapse-item>
        <el-collapse-item title="組別" name="3">
          <div class="order scrollbar">
            <el-check-tag
              v-for="(tag, idx) in tagsTeam"
              :key="`tag3_${idx}`"
              :checked="tag.checked"
              @change="onChange( 'tag', idx)"
              :class="{ tagChecked: tag.checked, tagUnchecked: !tag.checked }"
            >
              {{ tag.label }}
            </el-check-tag>
            <p class="no-use">
              Lorem ipsum dolor sit amet consectetur adipisicing elit. Dolor
              sequi harum deserunt eum eius aliquid temporibus velit quos.
              Recusandae commodi tenetur blanditiis omnis voluptates nesciunt
              dolores voluptas quam praesentium quia odit, veritatis modi
              consequuntur, amet atque iure rerum, quos accusantium cupiditate
              ad harum dignissimos! Dolores a neque pariatur atque incidunt
              quaerat culpa veniam quas officiis sequi sed vitae quod commodi,
              eveniet nobis officia consectetur aut, ab optio similique, placeat
              aspernatur. Laborum soluta minima expedita. Harum incidunt culpa
              porro, praesentium nulla ut blanditiis eaque iusto officia itaque
              reiciendis adipisci et aliquid facilis ipsa explicabo nam sequi ad
              laborum qui illum corporis.
            </p>
          </div>
        </el-collapse-item>
      </el-collapse>
    </div>
  </div>
</template>

<script>
import { ref } from "vue";
import axios from "axios";
import { useRouter } from "vue-router";

export default {
  name: "TagSearchArea",
  setup(props,{emit}) {
    const initials = ref(['a','b','c','d','e','f','g','h','i']);
    const router = useRouter();
    const selectedOptions = ref([]);
    const checked = ref(false);
    const options1 = Array.from({ length: 1000 }).map((_, idx) => ({
      key: `Option${idx + 1}`, // Assuming key is needed
      label: `${initials[idx % 10]}${idx}`,
    }));
    const activeNames = ref(["1"]);
    const handleChange = (val) => {
      console.log(val);
    };
    const tagsDate = ref([
      { label: "2021/10/12", checked: false },
      { label: "2022/10/12", checked: false },
      { label: "2023", checked: false },
      { label: "10/13", checked: false },
      { label: "10/14", checked: false },
      { label: "1014/01/12", checked: false },
    ]);
    const tagsThing = ref([
      { label: "早餐", checked: false },
      { label: "午餐", checked: false },
      { label: "開會", checked: false },
      { label: "事項", checked: false },
      { label: "重要", checked: false },
      { label: "非常重要", checked: false },
    ]);
    const tagsTeam = ref([
      { label: "前端", checked: false },
      { label: "後端", checked: false },
      { label: "美宣", checked: false },
      { label: "設計", checked: false },
      { label: "場佈", checked: false },
      { label: "視覺", checked: false },
    ]);

    const onChange = (tag, idx) => {
      goSearch();
      if(tag === "tagD"){
        const tagNow = tagsDate.value[idx];
        tagNow.checked = !tagsDate.value[idx].checked;
        tagsDate.value.sort((a,b) => b.checked - a.checked);
        if(tagNow.checked){
          selectedOptions.value.push(tagNow);
        }
      }
      else if(tag === "tag2"){
        const tagNow = tagsThing.value[idx];
        tagNow.checked = !tagsThing.value[idx].checked;
        tagsThing.value.sort((a,b) => b.checked - a.checked);
        if(tagNow.checked){
          selectedOptions.value.push(tagNow);
        }
      }
      else{
        const tagNow = tagsTeam.value[idx];
        tagNow.checked = !tagsTeam.value[idx].checked;
        arraySorter(tagsTeam);
        // tagsTeam.value.sort((a,b) => b.checked - a.checked);
        if(tagNow.checked){
          selectedOptions.value.push(tagNow);
        }
      }
      arrayFilter();
    };
    
    const goSearch = () => {
      if(selectedOptions.value != null) {
      // router.push('/searching');
        emit('showBlock',false);
      }
    };

    const arraySorter = (arrayGroup) => {
      arrayGroup.value.sort((a,b) => b.checked - a.checked);
    };

    const arrayFilter = () => {
      selectedOptions.value = selectedOptions.value.filter(tag => tag.checked !== false);
    };

    const deleteTag = (tag) => {
      tag.checked = false;
      // arraySorter();  //刪除後想要重新排序內部
      arrayFilter();
      console.log(tag.label);
    };
    

    return {
      selectedOptions,
      options1,
      activeNames,
      handleChange,
      checked,
      tagsDate,
      tagsThing,
      tagsTeam,
      onChange,
      goSearch,
      deleteTag,
    };
  },
};
</script>

<style scoped>
* {
  font-family: PingFang TC;
}
.tagSearchArea {
  width: 25%;
}
.tagSearchArea .trans {
  height: 1rem;
  width: 100%;
  opacity: 1;
  /* border: 2px solid black; */
}

.tagSearchArea .tagTypingArea .el-select {
  width: 100%;
}

.demo-collapse .el-collapse {
  width: 100%;
  /* border: 2px solid black; */
  box-shadow: 2px 2px 10px 1px rgba(0, 0, 0, 0.2);
  background: #fff;
}
.demo-collapse .el-collapse-item {
  display: flex;
  flex-wrap: wrap;
  border-bottom: 1px solid #e4e7ed;
  padding: 16px;
  color: var(--base-color-text-el-text-color-primary, #303133);
  font-family: PingFang TC;
  font-size: 16px;
  font-style: normal;
  font-weight: 600;
  line-height: 24px; /* 150% */
}
.demo-collapse .el-collapse-item * {
  display: flex;
  flex-wrap: wrap;
  
}
.no-use {
  font-size: 1px;
  color: white;
}
.order {
  display: flex;
  max-height: 24vh;
  border-top: #e4e7ed 1px;
  width: 97%;
  display: flex;
  overflow-y: scroll;
}
.scrollbar {
  &::-webkit-scrollbar {
    width: 8px;
  }
  &::-webkit-scrollbar-track {
    border-radius: 10px;
  }
  &::-webkit-scrollbar-thumb {
    border-radius: 10px;
    background-color: #e6e8eb;
  }
}
.no-use {
  font-size: 1px;
}

.tagChecked {
  color: white;
  font-family: PingFang TC;
  font-size: 13px;
  font-style: normal;
  font-weight: 400;
  line-height: 2vh;
  display: flex;
  justify-content: space-around;
  margin: 6px;
  background-color: #c91f2f;
  border: 1px solid #c91f2f;
}

.tagChecked:hover {
  background-color: #c91f2f;
}

.tagUnchecked {
  font-family: PingFang TC;
  font-size: 13px;
  font-style: normal;
  font-weight: 400;
  line-height: 2vh;
  display: flex;
  justify-content: space-around;
  margin: 6px;
  color: #c91f2f;
  border: 1px solid #f4cbcf;
  background-color: white;
}

.taglist{
 
}
</style>
