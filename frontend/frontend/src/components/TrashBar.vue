<template>
    <div id="navBar">
        <el-icon><fold/></el-icon>
        <div id="toolBar">
            <div id="icons">
                <button @click="searchClick" v-if="show"><a src="#"><el-icon class="icon"><search/></el-icon></a></button>
                <div class="icon" v-if="actived"><search-bar></search-bar></div>
                <button><el-icon class="icon"><lock/></el-icon></button>
                <!-- <button><el-icon class="icon"><bell/></el-icon></button> --> 
                <notification-menu class="icon"></notification-menu>
            </div>
            <user-info id="userInfo"></user-info>
            <el-icon><language/></el-icon>
            <!-- <img src="@/assets/language.svg" id="languageIcon"> -->
        </div>
    </div>
</template>


<script>
import { ref } from 'vue';
import NotificationMenu from './NotificationMenu.vue';
import UserInfo from './UserInfo.vue';
import SearchBar from './SearchBar.vue';
export default {
    components: {
        UserInfo,
        NotificationMenu,
        SearchBar,
    },
    setup() {
        const actived = ref(false);
        const show = ref(true);

        const searchClick = () => {
            actived.value = !actived.value;
            show.value = !show.value;

        };

        const reset = () => {
            actived.value = false;
            show.value = true;
        };
        return {
            normal: "#303133",
            actived,
            show,
            searchClick,
            reset,
        };
    },
}
</script>


<style scoped>
    #navBar{
        z-index: 5;
        position: fixed;
        left: 200px; 
        /* top: 0;  */
        display: flex;
        width: auto;
        height: 48px;
        padding: 0px 16px;
        justify-content: space-between;
        align-items: center;
        flex-shrink: 0;

        border-bottom: 1px solid #E4E7ED;
        background: #FFF;
        box-shadow: 0px 0px 12px 0px rgba(0, 0, 0, 0.12);
    }

    #breadCrumb{
        display: flex;
        position: absolute;
        left: 0;
        top: 0;
        padding: 12px 0 12px 16px;
        font-size: 14px;
    }
    #breadCrumb #first{
        color: #909399;
        font-size: 14px;
        font-style: normal;
        font-weight: 500;
        line-height: 24px; /* 171.429% */
    }

    #breadCrumb #now{
        color: #303133;
    }

    #toolBar{
        display: flex;
        position: absolute;
        right: 0;
        /* margin-right: 16px; */
        gap: 16px;
    }
    #icons{
        display: flex;
    }

    #icons button{
        border: none;
        background: none;
        cursor: pointer;
    }
    #icons .icon{
        display: flex;
        padding: 0px 12px;
        flex-direction: row;
        justify-content: center;
        align-items: center;
        align-self: stretch;
        cursor: pointer;
    }

    .el-dropdown-link{
        cursor: pointer;
    }

    #icon #languageIcon{
        display: block;
        /* padding: 16px 0; */
        justify-content: center;
        align-items: center;
        align-self: stretch;
    }

</style>