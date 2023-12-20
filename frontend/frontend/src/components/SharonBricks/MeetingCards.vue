<template>
    <div id="all" >
        <!-- @click="UnShow" -->
        <el-card id="box-card" @contextmenu="show" @click="nextPage">
            <img src="https://shadow.elemecdn.com/app/element/hamburger.9cf7b091-55e9-11e9-a976-7f4d0b07eef6.png">
            <div id="namePart">
                <span id="name">{{ record_name }}</span>
                <button @click.stop="show" ><i class="material-icons">&#xe5d2</i></button>
                <!-- @click.stop -->
            </div>
            <div id="tagPart" >
                <el-tag class="tag" v-for="item in 8" :key="item">標籤</el-tag>
                <el-tag class="tag">新增標籤</el-tag>
                <!-- @click="UnShow" -->
            </div>
        
        </el-card>
        <div v-if="isShowed" id="rightClick" ref = "rightClick" @click="unShow"><card-right-click  /></div>

    </div>
</template>

<script>

import { onUnmounted, ref, watch} from 'vue';
import CardRightClick from './CardRightClick.vue';
import { RouterLink } from 'vue-router';
import { useRouter } from "vue-router";
export default{
    components:{
        CardRightClick,
    },
    props:{
        isShowed: Boolean,
    },

    setup(props,{emit}){
        const router = useRouter;
        const isShowed= ref(false);
        const url = "https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png";
        const normal = "#303133";
        const record_name = "會議記錄";
        // ParentIsShowed = false;
        // const buttonRef = ref(null);

        const show = () => {
            isShowed.value = !isShowed.value;
        };

        const unShow = () => {
            isShowed.value = !isShowed.value;
            // console.log(value);
        };

        const nextPage = () => {
            emit("showMeeting", true);
        };

        // watch(() => {
        //     isShowed.value = props.isShowed;
        //     console.log(isShowed.value);
        // })

        // const nextPage = () => {
        //     router.push({ name: });
        // };


        // 點擊非指定區域
        const clickOut = (event) => {
            if(isShowed && !this.$ref.rightClick.contains(event.target)){
                unShow();
            }
        };

        // mounted (()=>{
        //     window.addEventListener('click' , clickOut);
        // });

        // onMounted(() => {
        //     window.addEventListener('click', clickOut);
        // });
           
        onUnmounted(()=>{
            window.addEventListener('click' , clickOut);
        });
        



        return{
            show,
            normal,
            url,
            record_name,
            isShowed,
            unShow,
            nextPage,
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
        border: 1px solid var(--base-color-primary-el-color-primary-8, #F4CBCF);    
        background: var(--base-color-fill-el-fill-color-blank, #FFF);

        color: var(--base-color-danger-el-color-danger, #C91F2F);
        text-align: center;

        /* CN regular/body2-Regular */
        font-family: PingFang TC;
        font-size: 13px;
        font-style: normal;
        font-weight: 400;   
        line-height: 22px; /* 169.231% */
    }
    .material-icons{
        font-size: 16px;
    }

    #namePart > button{
        border: none;
        background: none;
        position: absolute;
        right: 0;
        cursor: pointer;
    }

    #rightClick{
        position: absolute;
        top: 285px;
        left: 285px;
        z-index: 10;
    }
</style>