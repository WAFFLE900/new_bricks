import { createStore } from "vuex";

const store = createStore({
    state:{
        activeIndex: '/',
    },
    mutations:{
        updateActiveIndex(state,index){
            state.activeIndex = index;
        },
    },
});

export default store;