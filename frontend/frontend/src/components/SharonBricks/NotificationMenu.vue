<template>
    <el-dropdown trigger="click" max-height=480px >
        <span class="el-dropdown-link">
            <el-icon class="icon"><bell/></el-icon>
        </span>
        <template #dropdown>
            <el-dropdown-menu class="dropDown" >
                <div id="content">
                    <el-tabs v-model="activeName" class="tab" stretch model-value="first" tab-position="top">
                        <el-tab-pane label="總覽" name="first" >
                                <div class="contentCard">
                                    <el-scrollbar max-size="480px" class="scrollBar">
                                        <noti-content v-for="item in 4" :key="item"></noti-content>
                                    </el-scrollbar>
                                </div>
                            
                        </el-tab-pane>
                        <el-tab-pane label="提及" name="second">
                            <div class="contentCard">
                                    <el-scrollbar max-size="480px" class="scrollBar">
                                        <noti-content v-for="item in 4" :key="item"></noti-content>
                                    </el-scrollbar>
                                </div>
                        </el-tab-pane>
                        <el-tab-pane label="系統" name="third">
                            <div class="contentCard">
                                    <el-scrollbar max-size="480px" class="scrollBar">
                                        <noti-content v-for="item in 4" :key="item"></noti-content>
                                    </el-scrollbar>
                                </div>
                        </el-tab-pane>
                    </el-tabs>
                </div>

                <!-- <el-dropdown-item class="dropDown"><el-icon><user/></el-icon><span class="text">個人檔案</span></el-dropdown-item>
                <el-dropdown-item class="dropDown"><el-icon><span class="material-icons">help_outline</span></el-icon><span class="text">問題回報</span></el-dropdown-item>
                <el-dropdown-item class="dropDown"><el-icon><span class="material-icons">desktop_windows</span></el-icon><span class="text">介面教學</span></el-dropdown-item>
                <el-dropdown-item class="dropDown"><el-icon><i class="material-icons">exit_to_app</i></el-icon><span class="text">登出</span></el-dropdown-item> -->
            </el-dropdown-menu>
        </template>
    </el-dropdown> 
</template>

<script>
import NotiContent from './NotiContent.vue';
export default {
    setup(){

        return{

        };
    },
    components:{
        NotiContent,
    }
}
</script>

<style scoped>

    .dropDown{
        width: fit-content;
        padding: 12px;
        overflow:auto;
        height: 100%;
    }

    #content{
        width: fit-content;
        /* position: absolute; */
    }

    .tab{
        position: sticky;
        height: 100%;
        /* top: 0; */

    }

    .contentCard{
        /* position: absolute; */
        top: 42px;
    }


</style>