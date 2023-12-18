<template>
    <el-dropdown trigger="click" class="dropdown">
          <span class="el-dropdown-link">
            排序<el-icon class="el-icon--right"><sort/></el-icon>
          </span>
          <template #dropdown>
            <el-dropdown-menu class="menu">
              <el-dropdown-item ><span class="dropdownMenu">最近</span ></el-dropdown-item>
              <el-dropdown-item ><span class="dropdownMenu">最遠</span></el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
  </template>
  
  <script>
  export default {
  
  }
  </script>
  
  <style scoped>
      .el-dropdown-link .el-icon--right{
          color: #C91F2F;
      }
  
      .dropdown{
          border-radius: var(--radius-button-small-radius, 2px);
          border: 1px solid var(--base-color-border-el-border-color-light, #E4E7ED);
          background: var(--base-color-el-color-white, #FFF);
          cursor: pointer;
  
      }
      
      .dropdown>span{
          color: #C91F2F;
          /* padding: 4px 16px; */
          display: flex;
          height: var(--size-button-button-size-default, 32px);
          min-height: 24px;
          max-height: 40px;
          padding: var(--space-size-4, 4px) var(--space-size-large, 16px);
          justify-content: center;
          align-items: center;
          gap: var(--space-size-small, 8px);
      }
      
      .dropdownMenu{
          width: 80px;
          padding: 4px 12px;
          color: var(--base-color-text-el-text-color-primary, #303133);
  
          /* CN regular/body1-Regular */
          font-family: PingFang TC;
          font-size: 14px;
          font-style: normal;
          font-weight: 400;
          line-height: 24px; /* 171.429% */
      }
  
      .menu :hover{
          color: #C91F2F;
          background-color: #FAE4E7;
      }
  
  </style>