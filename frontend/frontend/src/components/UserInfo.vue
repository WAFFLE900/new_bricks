<template>
    <el-dropdown trigger="click">
        <span class="el-dropdown-link">
            <div id="userInfo">
                <el-avatar shape="square" :size="size" :src=squareUrl id="avatar" />
                <p>{{ user_name }}</p>
            </div>
        </span>
        <template #dropdown>
          <el-dropdown-menu id="dropDown">
            <el-dropdown-item :icon="Plus" class="firstDrop">
                <div id="userInfoInside">
                    <el-avatar shape="square" :size=80 :src=squareUrl id="avatarInside" />
                    <p>{{ user_name }}</p>
                </div>
            </el-dropdown-item>
            <el-dropdown-item>
                <div class="dropDown">
                    <el-icon class="material-icons"><user/></el-icon ><span class="text">個人檔案</span>
                </div>
            </el-dropdown-item>
            <el-dropdown-item>
                <div class="dropDown">
                    <el-icon><span class="material-icons">help_outline</span></el-icon><span class="text">問題回報</span>
                </div>
            </el-dropdown-item>
            <el-dropdown-item >
                <div class="dropDown">
                    <el-icon><span class="material-icons">desktop_windows</span></el-icon><span class="text">介面教學</span>
                </div>
            </el-dropdown-item>
            <el-dropdown-item >
                <div class="dropDown">
                    <el-icon><i class="material-icons">exit_to_app</i></el-icon><span class="text">登出</span>
                </div>
            </el-dropdown-item>
          </el-dropdown-menu>
        </template>
      </el-dropdown>    
    
    
</template>

<script>
export default {
    setup(){
        return{
            user_name: "Designer",
            squareUrl: "https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png",
        };
    },
    methods:{

    }
}
</script>

<style scoped>
    #userInfo{
        display: flex;
        /* padding: 0px 0px; */
        align-items: center;
        gap: 8px;
        align-self: stretch;
        cursor: pointer;
    }

    #userInfo p{
        color: #303133;
        font-family: Noto Sans TC;
        font-size: 14px;
        font-style: normal;
        font-weight: 400;
        line-height: 24px; /* 171.429% */
        /* cursor: pointer; */
    }

    #userInfo #avatar{
        height: 32px;
        width: auto;
    }

    .dropDown{
        cursor: pointer;
        display: flex;
        /* gap: 4px; */
        /* width: 200px; */
        padding: 8px;
        height: auto;
        justify-content:center;
        align-items: center;
        padding-left: 12px;
    }

    .dropDown .text{
        display: block;
        color: var(--base-color-text-el-text-color-primary, #303133);
        /* CN regular/body1-Regular */
        font-family: PingFang TC;
        font-size: 14px;
        font-style: normal;
        font-weight: 400;
        line-height: 24px; /* 171.429% */
        padding-left: 4px;
        text-align: left;
        margin-left: 4px;
    }

    #userInfoInside{
        display: flex;
        padding: 16px;
        align-items: center;
        /* gap: 20px; */

        color: #000;
    }
    #userInfoInside #avartarInside{
        width: 56px;
        height: 56px;
    }

    #userInfoInside p{
        font-family: PingFang TC;
        font-size: 20px;
        font-style: normal;
        font-weight: 400;
        line-height: 28px; /* 140% */
        padding-left: 14px;
    }

    .material-icons { 
        font-size: 18px; 
    }
</style>