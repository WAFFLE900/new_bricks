<template>
    <div id="all" @click.right.prevent>
        <el-card id="box-card" @click.right="show" @click="unshown">
            <img src="https://shadow.elemecdn.com/app/element/hamburger.9cf7b091-55e9-11e9-a976-7f4d0b07eef6.png">
            <div id="namePart">
                <span id="name">{{ record_name }}</span>
            </div>
            <div id="tagPart">
                <el-tag class="tag" v-for="item in 8" :key="item">標籤</el-tag>
                <el-tag class="tag">新增標籤</el-tag>

            </div>
        
        </el-card>
        <!-- v-if="isShowed" -->
        <div id="rightClick" v-if="isShowed">
            <div id="container">
                <span id="recover" @click="recover">復原</span>
                <span id="delete" @click="deleteForever"><deleteForever/>永久刪除</span>
            </div>
        </div>
    </div>
</template>

<script>

import { ref } from 'vue';
// import DeleteForever from '../KarenBricks/DeleteForever.vue';
import { ElNotification } from 'element-plus';
import { ElMessage } from 'element-plus';

export default {
    components:{
        
    },

    setup(){
        
        const isShowed= ref(false);
        const url = "https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png";
        const normal = "#303133";
        const record_name = "會議記錄";
        // ParentIsShowed = false;
        // const buttonRef = ref(null);

        const show = () => {
            isShowed.value = !isShowed.value;
        };

        const unshown = () => {
            isShowed.value = false;
        };

        const deleteForever = () => {
            ElMessage('您已永久刪除會議記錄')
        }; 

        const recover = () => {
            ElNotification({
                dangerouslyUseHTMLString: true,
                title: '成功復原會議記錄',
                message: '<a href="/path/to/recovery/file" style="color: #67C23A; text-decoration: underline;">點擊檢視復原檔案</a>',
                type: 'success',
                position: 'bottom-right',
            });
        };


        return{
            show,
            normal,
            url,
            record_name,
            isShowed,
            unshown,
            deleteForever,
            recover,
        };

        

    },
};
    
</script>

<style scoped>
    #all{
        position: relative;
    }
    #box-card{
        display: flex;
        padding: 0 16px;
        flex-direction: column;
        align-items: center;
        text-align: left;
        gap: 12px;
        width: 244px;
        height: auto;
        position: relative;
        cursor: pointer;
    }

    #img{
        display: block;
        /* padding: 0; */
        height: 200px;
        width: auto;
        /* cursor:all-scroll; */
    }
    #namePart{
        position: relative;
        display: flex;
        padding: 16px 16px 16px 0;
        align-items: center;
        /* justify-content: center; */
    }
    #name{
        text-align: left;
        color: var(--base-color-text-el-text-color-primary, #303133);

        /* CN medium/Headline3-Medium */
        font-family: PingFang TC;
        font-size: 16px;
        font-style: normal;
        font-weight: 600;
        line-height: 24px; /* 150% */
    }

    #namePart:hover{
        cursor: pointer;
        text-decoration: underline;
        /* font-weight: 600; */
    }

    #namePart img{
        position: absolute;
        right: 0;
        width: 18px;
        height: 18px;
    }

    #tagPart{
        padding: 0;
        display: flex;
        justify-content: left;
        width: 230px;
        height: 60px;
        flex-wrap: wrap;
        gap: 12px;
        overflow: hidden;
    }
    .tag{
        width: fit-content;
        flex-direction: column;
        display: flex;
        padding: 1px 10px;
        justify-content: center;
        align-items: center;

        border-radius: var(--radius-button-large-radius, 4px);
        border: 1px solid var(--base-color-info-el-color-info-5, #C8C9CC);
        background: var(--base-color-fill-el-fill-color-blank, #FFF);

        color: var(--base-color-info-el-color-info, #909399);
        text-align: center;

        /* CN regular/body2-Regular */
        font-family: PingFang TC;
        font-size: 13px;
        font-style: normal;
        font-weight: 400;
        line-height: 22px; /* 169.231% */
    }

    #rightClick{
        display: flex;
        flex-direction: row;
        width: 116px;
        height: auto;
        flex-wrap: wrap;
        padding: 8px 0;
        border-radius: var(--radius-button-large-radius, 4px);
        border: 1px solid var(--base-color-border-el-border-color-light, #E4E7ED);
        background: var(--base-color-fill-el-fill-color-blank, #FFF);
        /* light/--el-box-shadow */
        box-shadow: 0px 12px 32px 4px rgba(0, 0, 0, 0.04), 0px 8px 20px 0px rgba(0, 0, 0, 0.08);
        position: absolute;
        top: 285px;
        left: 285px;
        z-index: 10;
    }
    #container{
        display: block;
        /* font-size: 10px; */
        width: 116px;
        padding: 8px 0;
    }

    #container > span{
        color: var(--base-color-text-el-text-color-primary, #303133);
        font-family: Noto Sans TC;
        font-size: 14px;
        font-style: normal;
        /* font-weight: 400; */
        line-height: 24px; /* 171.429% */
        text-align: left;
        padding: 8px 12px;
        cursor: pointer;
    }

    #container > span:hover{
        color: #C91F2F;
        background-color: #FAE4E7;
    }

    #recover{
        display: block;
        /* font-size: 10px; */
    }

    #delete{
        display: block;
    }

</style>