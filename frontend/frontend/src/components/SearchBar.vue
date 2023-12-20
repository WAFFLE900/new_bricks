<template>
    <el-autocomplete
        
        v-model="state1"
        :fetch-suggestions="querySearch"
        clearable
        class="inline-input"
        placeholder="搜尋會議紀錄或內文"
        @select="handleSelect"
        id="search"
        popper-class="popMenu"
        :popper-append-to-body="false"
    >
    <template #prefix>
      <el-icon class="el-input__icon" @click="handleIconClick">
        <search />
      </el-icon>
    </template>
    
    <template #default="{ item }" >
        <div class="value" >{{ item.value }}</div>
        <!-- <span class="link">{{ item.link }}</span> -->
    </template>

    </el-autocomplete>
  
</template>

<script>
import { onMounted, ref } from 'vue';
export default {
    setup(){
        const state1 = ref('');
        const state2 = ref('');

        const restaurants = ref([]);
        const querySearch = (queryString, cb) => {
            const results = queryString ? restaurants.value.filter(createFilter(queryString)) : restaurants.value;
            // 調用回調函數返回建議
            cb(results);
        };

        const createFilter = (queryString) => {
            return (restaurant) => {
                return restaurant.value.toLowerCase().indexOf(queryString.toLowerCase()) === 0;
            };
        };

        const loadAll = () => {
            return [
                { value: '搜尋紀錄一' },
                { value: '搜尋紀錄二' },
                { value: '搜尋紀錄三' },
                { value: '搜尋紀錄四' },
                { value: '搜尋紀錄五' },
                { value: '搜尋紀錄六'},
                { value: '搜尋紀錄七' },
            ];
        };

        const handleSelect = (item) => {
            console.log(item);
        };

        onMounted(() => {
            restaurants.value = loadAll();
        });

        return{
            state1,
            state2,
            restaurants,
            querySearch,
            createFilter,
            loadAll,
            handleSelect,
        };
    }
}
</script>

<style scoped>

    #search{
        width: 200px;
    }

    ::v-deep .inline-input {

    }

</style>