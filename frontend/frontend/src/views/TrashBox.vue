<template>
    <side-bar class="sideBar" @update="selectedItemUpdate" @showAdd="show" :activeIndex="currentActive"></side-bar>
    <div class="navAndCont" id="trash">
        <trash-bar class="navBar"></trash-bar>
        <div class="cards">
            <trash-cards v-for="items in 16" :key="items"></trash-cards>
        </div>
    </div>
</template>

<script>
import SideBar from '../components/SideBar.vue';
import TrashBar from '../components/TrashBar.vue';
import TrashCards from '../components/TrashCards.vue';
export default {
    name : 'trashBox',
    components : {
        SideBar,
        TrashBar,
        TrashCards,

    },
    setup(){
        return{

        };
    }

}
</script>

<style scoped>
.navBar{
    position: absolute;
    top: 0;
    left: 200px;
    right: 0;
    /* grid-area: navBar; */
 }
 .sideBar{
    /* grid-area: sideBar; */
    position: absolute;
    top: 0;
    left: 0;
    bottom: 0;
}
.cards{
  display: grid;
  grid-column-gap:16px;
  grid-row-gap:20px;
  grid-template-columns: 1fr 1fr 1fr 1fr;
  margin: 28px 10vw 28px 28px;

  position: absolute;
  top: 48px;
  /* border: 1px; */
 }
 .navAndCont{
  background-color: #DCDFE6;
  position: absolute;
  left: 200px;
  width:auto;
  top: 0;
  right: 0;
 }

</style>