<template>
  <div class="box-card">
    <div class="text">
        <p>{{ content }}</p>
    </div>
    <div id="footer">
        <div id="user">
            <el-avatar shape="circle" size=28 :src=circleUrl id="avatar" />
            <el-text>{{ name }}</el-text>
        </div>
        <div id="icon">
            <el-icon><i class="material-icons">&#xe2e6</i></el-icon>
        </div>
    </div>
</div>
</template>

<script>
export default {
    setup(){
        return{
            content: "@everyone 我們上次的討論結果是中文用 Noto Sans TC 英文及標點符號用Noto Sans，用中文的原...對對對度對對",
            circleUrl: "@/assets/Rectangle.png",
            name: "某人名字",
        };
    }

}
</script>

<style scoped>
    .box-card{
        display: flex;
        padding: var(--space-size-large, 16px);
        flex-direction: column;
        align-items: center;
        gap: var(--space-size-default, 12px);
        align-self: stretch;

        height: 132px;
        width: 200px;
        border-radius: var(--radius-button-no-radius, 4px);
        background: var(--base-color-info-el-color-info-9, #F4F4F5);
        box-shadow: none;
        position: relative;
        margin-bottom: 8px;
    }

    .text {
        word-wrap:break-word;
        white-space: pre-wrap;
        height: 68px;
        width: 184px;
        overflow: hidden;

        color: #404040;
        /* text-overflow: ellipsis; */

        /* CN regular/body3-Regular */
        font-family: Helvetica;
        font-size: 12px;
        font-style: normal;
        font-weight: 400;
        line-height: 20px; /* 166.667% */
    }

    #user{
        position: absolute;
        left: 0;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 8px;
        /* padding: 2; */
    }

    #footer{
        display: flex;
        flex-direction: column;
        position: relative;
        width: 184px;
        align-items: center;
        justify-content: center;
        top: 24px;
    }

    #icon{
        position: absolute;
        right: 0;
        padding: 6px 0;
        /* justify-content: center; */
        /* padding: auto 0; */
        /* align-items: center; */
    }

    .material-icons{
        font-size: 16px;
        
    }


</style>