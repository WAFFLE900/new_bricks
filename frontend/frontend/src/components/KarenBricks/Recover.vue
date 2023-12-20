<template>
    <el-alert class="popUp_recover"
        title="成功復原會議紀錄"
        type="success"
        show-icon
        :style="{ backgroundColor: '#FFFFFF'}"
        >
        <!-- 不知道怎麼單獨改title的顏色，因為title的屬性好像是跟著圖標的 -->
        <a href="link-url" :style="{ color: '#67C23A' }">點擊檢視復原檔案</a>
    </el-alert>
</template>
<script>

</script>

<style>
.popUp_recover {
  width: 481px;
  height: 80px;
  position: fixed;
  bottom: 0;
  right: 0;
  margin: 40px;
  box-shadow: 0 5px 8px rgba(0, 0, 0, 0.4); 
}
</style>