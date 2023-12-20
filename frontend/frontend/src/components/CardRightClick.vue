<template>
    <div id="card">
        <div id="container" >
            <span id="copy" @click="copyLink">複製連結</span>
            <span id="delete" @click="deleteRecord">刪除會議記錄</span>
        </div>
    </div>
    <div ref="containerRef">
    <!-- 點擊外部時觸發的區域 -->
    </div>
</template>

<script>
import { ref } from 'vue';
import { ElMessage } from 'element-plus';
import {  onMounted, onBeforeUnmount } from 'vue';
export default {
    
    setup(props,{emit}){
        // const containerRef = ref(null);
        // const status = ref(false);

        // const handleClickOutside = (event) => {
        //     const container = containerRef.value;
        //     console.log('handleClickOutside called');


        //     // 检查点击的目标是否在 container 之外
        //     if (container && !container.contains(event.target)) {
        //         console.log('Clicked outside the container');

        //         status.value = false;
        //         emit('chosen', status.value);
        //     }
        // };
        // onMounted(() => {
        //     // 在页面上添加点击事件监听器
        //     console.log('Event listener added');
        //     document.addEventListener('click', handleClickOutside);
        // });

        // onBeforeUnmount(() => {
        // // 在组件销毁前移除点击事件监听器，以防内存泄漏
        // document.removeEventListener('click', handleClickOutside);
        // });

        const change = (status) => {
            status = false;
            emit('chosen', status);
        };
        
        const copyLink = () => {
            ElMessage({
                message: '會議記錄連結已複製',
                type: 'success',
                position: 'bottom-right',
            });

            // status = false;
            // emit('clicked',false)
        };
        const deleteRecord =()=>{
            ElMessage.error('您已刪除會議記錄');
            // status = false;
            // emit('clicked',status)
        };
        return{
            change,
            status,
            copyLink,
            deleteRecord,
        }
    }
}
</script>

<style scoped>
    #card{
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

    #copy{
        display: block;
        /* font-size: 10px; */
    }

    #delete{
        display: block;
    }
</style>