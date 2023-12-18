<template>
    <side-bar class="sideBar" @update="selectedItemUpdate" @showAdd="show" ></side-bar>
    <!-- :activeIndex="currentActive" -->

    <div class="navAndCont" id="cards">
      <nav-bar-all class="navBar" @click="StopShowing"></nav-bar-all>
      <div class="cards">
        <meeting-cards v-for="items in 16" :key="items" :isShowed="isShowed" @showMeeting="show"></meeting-cards>
      </div>
    </div>
</template>

<script>
import NavBarAll from '../components/NavBarAll.vue';
import SideBar from '../components/SideBar.vue';
import MeetingCards from '../components/MeetingCards.vue';
import { ref } from 'vue';

export default {
    name: 'recordCard',
    components: {
        SideBar,
        NavBarAll,
        MeetingCards,
        
    },
    setup(props,{emit}){

        const currentActive = ref("1-1");

        return{
            currentActive,

        };
    },

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