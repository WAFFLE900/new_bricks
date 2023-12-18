<template>
  <div style="width: 100%; position: absolute; left: 0; top: 0">
    <div class="nav">
      <img src="../assets/brickslogo.svg" @click="" />
      <div class="tri_btn">
        <input type="text" />
        <img src="../assets/search.svg" alt="" class="search" />
        <img src="../assets/Notice/Notice_Default.svg" alt="" class="notice" />
        <img
          src="../assets/Profile/Profile_Default.svg"
          alt=""
          class="profile"
        />
      </div>
    </div>
    <div class="left_bar">
      <div class="add_btn" @click="add_btn">新增專案</div>
      <div class="plus" @click="add_btn"></div>
      <div class="three_pointer">
        <input
          type="radio"
          id="overview"
          class="list"
          name="list"
          value="option1"
          v-model="selectOption"
        />
        <label for="overview" @click="change(1)">專案總覽</label>
        <img src="../assets/icon/icon_file.svg" style="top: 26px" />
        <input
          type="radio"
          id="over"
          class="list"
          name="list"
          value="option2"
          v-model="selectOption"
        />
        <label for="over" @click="change(2)">已結束專案</label>
        <img src="../assets/icon/icon_over.svg" style="top: 102px" />
        <input
          type="radio"
          id="trash"
          class="list"
          name="list"
          value="option3"
          v-model="selectOption"
        />
        <label for="trash" @click="change(3)">垃圾桶</label>
        <!-- v-on:click="show_trashcan" -->
        <img src="../assets/icon/icon_trashcan.svg" style="top: 178px" />
      </div>
    </div>
    <div class="add_proj_box" v-show="add_proj_show">
      <div
        class="close_add_proj_box"
        @click="
          add_btn();
          close_add_proj();
        "
      ></div>
      <p class="add_proj_title">新增專案</p>
      <div class="add_proj_pic">
        <img src="../assets/add_proj_pic_plus.svg" class="add_proj_pic_plus" />
      </div>
      <input
        type="text"
        placeholder="輸入專案名稱"
        class="add_proj_name"
        v-model="add_proj_name"
      />
      <div
        class="add_proj_type"
        @click="add_proj_type_btn"
        :style="{ background: add_proj_type_arrow, color: proj_type_color }"
        ref="add_proj_type"
      >
        {{ proj_type }}
      </div>
      <div
        class="add_proj_type_list"
        v-show="show_add_proj_type_list"
        ref="add_proj_type_list"
      >
        <div class="add_proj_type_option" @click="type_not_choose">未分類</div>
        <div
          v-for="(option, index) in add_proj_type_options"
          :key="index"
          class="add_proj_type_option"
          @click="type_choosen(option)"
        >
          {{ option }}
        </div>
        <div class="add_proj_type_list_line"></div>
        <input
          type="text"
          class="add_proj_type_text"
          placeholder="新增類別"
          v-model="add_proj_type_text"
          @keyup.enter="list_add_a_cart"
        />
        <div class="add_proj_type_text_plus" @click="list_add_a_cart"></div>
      </div>
      <div class="add_proj_build" @click="new_project_btn">建立專案</div>
    </div>
    <div class="main_body">
      <div class="bg">
        <!-- 背景透明灰色 -->
        <div class="overlay" v-if="showOverlay"></div>
        <div class="middle">
          <!-- 專案總覽 -->
          <div class="overview_page" v-show="middle_show_overview_page">
            <div class="uncategorized cart" ref="uncategorized">
              <p class="cart_title">未分類</p>
              <div class="title_underline"></div>
              <div class="box_container">
                <div
                  class="box"
                  v-for="(proj_name, index) in uncategorized_projs"
                  :key="index"
                  @contextmenu.prevent="right_click_box"
                >
                  {{ proj_name }}
                </div>
              </div>
            </div>
            <div v-for="(cart, index1) in carts" :key="index1">
              <div class="cart">
                <p class="cart_title" style="height: 0px">
                  {{ cart.title_word }}
                </p>
                <img
                  src="../assets/cart_drag_icon.svg"
                  alt=""
                  class="cart_drag_icon"
                />
                <div class="title_underline"></div>
                <div class="box_container">
                  <div
                    class="box"
                    v-for="(proj_name, index2) in carts[index1].project_box"
                    :key="index2"
                    @contextmenu.prevent="right_click_box"
                  >
                    {{ proj_name }}
                  </div>
                </div>
              </div>
            </div>
            <div
              class="new_type cart"
              :class="{ new_type_highlight: isFocused }"
            >
              <input
                class="cart_title_input"
                placeholder="新增類型"
                @focus="new_type_focus"
                @blur="new_type_blur"
                @keyup.enter="add_a_cart"
                v-model="cart_title_input"
              />
              <div class="title_underline"></div>
              <div class="box_container"></div>
            </div>
            <div
              class="right_click_box_overview"
              :style="{ top: mouseTop + 'px', left: mouseLeft + 'px' }"
              v-show="right_click_box_overview_show"
              ref="right_click_box_overview"
            >
              <div
                class="right_click_box_overview_option"
                style="
                  border-top-left-radius: 5px;
                  border-top-right-radius: 5px;"
                
                @click=" "
              >
                重新命名
              </div>
              <div class="add_proj_type_list_line"></div>
              <div
                class="right_click_box_overview_option"
                style="
                  border-bottom-left-radius: 5px;
                  border-bottom-right-radius: 5px;
                "
                @click="delete_project"
              >
                刪除專案
              </div>
            </div>
            <div class="delete_confirm" v-show="delete_confirm">
              <div
                class="close_delete_confirm"
                @click="close_delete_confirm"
              ></div>
              <p class="delete_confirm_first_text">刪除專案</p>
              <img src="../assets/delete_icon.svg" alt="" />
              <p class="delete_confirm_second_text">確定刪除專案？</p>
              <p class="delete_confirm_third_text">
                刪除後若需還原，請至「垃圾桶」查看
              </p>
              <div class="delete_confirm_btn_container">
                <button
                  class="forever_delete_confirm_btn forever_delete_confirm_btn_cancel"
                  @click="close_delete_confirm"
                >
                  取消
                </button>
                <button
                  class="forever_delete_confirm_btn forever_delete_confirm_btn_delete"
                  @click="delete_project_click"
                >
                  刪除
                </button>
              </div>
            </div>
            <div class="overlay" v-if="showOverlay_delete"></div>
          </div>
          <!-- 已結束專案 -->
          <div class="over_page" v-show="middle_show_over_page">
            <!-- <div class="uncategorized cart" ref="uncategorized">
                            <p class="cart_title">未分類</p>
                            <div class="title_underline"></div>
                            <div class="box_container">
                                <div class="box" v-for="(proj_name,index) in uncategorized_projs" :key="index">{{ proj_name }}</div>
                            </div>
                        </div> -->
                        <div class="uncategorized cart" ref="uncategorized">
                            <p class="cart_title">未分類</p>
                            <div class="title_underline"></div>
                            
                            <div class="box_container">
                              <!-- <div v-if="cart.project_ended">  設定只有結束的專案才能跑進來 -->
                                <div class="box" v-for="(proj_name,index) in ended_projects" :key="index">{{ proj_name }}</div>
                              <!-- </div> -->
                            </div>
                        </div>
                        <div v-for="(endParts,index1) in ended_projects" :key="index1">
                            <div class="cart">
                                <p class="cart_title" style="height: 0px">{{ endParts.tit }}</p>
                                <img src="../assets/cart_drag_icon.svg" alt="" class="cart_drag_icon">
                                <div class="title_underline"></div>
                                <div class="box_container">
                                    <div class="box" v-for="(proj_name,index2) in ended_projects[index1].project_box" :key="index2" >{{ proj_name }}</div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <!-- 垃圾桶 -->
                    <div class="trash_page" v-show="middle_show_trash_page">
                        <div class="trash_page_middle">
                            <div class="last_30_days">
                                <p class="last_time">近 30 天</p>
                                <div class="time_subline"></div>
                                <img v-if="recover" src="../assets/trash_page/recover_default.svg" alt="" class="recover_trash_pic" >
                                <img v-else src="../assets/trash_page/recover_active.svg" alt="" class="recover_trash_pic" style="cursor: pointer;" @click="recover_project">
                                <img v-if="trashcan" src="../assets/trash_page/trashcan_default.svg" alt="" class="forever_delete trash_pic">
                                <img v-else src="../assets/trash_page/trashcan_active.svg" alt="" class="forever_delete trash_pic" style="cursor: pointer;" @click="forever_delete_project">
                                <div class="trash_box_container">
                                    <div class="trash_box" v-for="(trash_box,index) in trash_boxes" :key="index" >
                                        <input type="checkbox" :id="'trash_box-' + index" v-model="checked_trash_box[index]" @change="selected_trash_box(index)" >
                                        <label :for="'trash_box-' + index" @contextmenu.prevent="right_click_box_trash">{{trash_box.text}}</label>
                                    </div>
                                </div>
                            </div>
                            <div class="last_one_year">
                                <p class="last_time">近一年</p>
                                <div class="time_subline"></div>
                                <div class="trash_box_container"></div>
                            </div>
                            <div class="recovered" v-show="recovered">
                                <img src="../assets/recovered_icon.svg" alt="">
                                <p>檔案已還原</p>
                            </div>
                            <div class="forever_delete_confirm" v-show="forever_delete_confirm">
                                <div class="close_forever_delete_confirm" @click="close_forever_delete_confirm"></div>
                                <p class="forever_delete_confirm_first_text">永久刪除專案</p>
                                <img src="../assets/forever_delete_icon.svg" alt="">
                                <p class="forever_delete_confirm_second_text">確定永久刪除專案？刪除後將無法復原</p>
                                <div class="forever_delete_confirm_btn_container">
                                    <button class="forever_delete_confirm_btn forever_delete_confirm_btn_cancel" @click="close_forever_delete_confirm">取消</button>
                                    <button class="forever_delete_confirm_btn forever_delete_confirm_btn_delete" @click="forever_delete_project_delete">刪除</button>
                                </div>
                            </div>
                            <div class="overlay" v-if="showOverlay_trash"></div>
                            <div class="right_click_box_overview" :style="{top: mouseTop +'px', left: mouseLeft + 'px'}" v-show="right_click_box_trash_show" ref="right_click_box_trash">
                                <div class="right_click_box_overview_option" style="border-top-left-radius: 5px; border-top-right-radius: 5px;" @click="recover_project">還原專案</div>
                                <div class="add_proj_type_list_line"></div>
                                <div class="right_click_box_overview_option" style="border-bottom-left-radius: 5px; border-bottom-right-radius: 5px;" @click="forever_delete_project">刪除專案</div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  export default {
    name: 'Personal_homepage',
    data() {
        return {
            middle_show_overview_page: true,
            middle_show_over_page: false,
            middle_show_trash_page: false,
            add_proj_show: false,
            showOverlay: false,
            add_proj_type: '',
            isFocused: false,
            carts:[],
            cart_titles: '',
            cart_title_input: '',
            selectOption: 'option1',
            show_add_proj_type_list: false,
            add_proj_type_arrow: '',
            add_proj_type_options: [],
            proj_type: '選擇專案類型',
            proj_type_color: '#b6aeae',
            add_proj_type_text: '',
            add_proj_name: '',
            uncategorized_projs: [],
            // cart_box_name_list: [],   沒用到
            trash_boxes: [],
            checked_trash_box: [],
            recover: true,
            trashcan: false,
            recovered: false,
            // ended: false,
            forever_delete_confirm: false,
            showOverlay_trash: false,
            mouseTop: 0,
            mouseLeft: 0,
            right_click_box_overview_show: false,
            delete_confirm: false,
            showOverlay_delete: false,
            right_click_box_trash_show: false,
            ended_projects: [],
            project_box: [],
  
            projects:[],
            user_id: 1,
            project_name: "",
            project_id: 0,
            getPath: "http://35.194.196.179:5000/project_index",
  
            found_project: null,
        };
    },
    methods: {
        // 點擊上角新增專案
        // 取值
        
        add_btn() {
            this.add_proj_show = this.add_proj_show === false ? true : false;
            this.showOverlay = !this.showOverlay;
            this.proj_type = '選擇專案類型';
            this.proj_type_color = '#b6aeae';
            this.add_proj_name = '';
            this.forever_delete_confirm = false;
            this.showOverlay_trash = false;
            this.add_proj_type_text = '';
            this.show_add_proj_type_list = false;
            this.delete_confirm = false;
            this.showOverlay_delete = false;
        },
        // 新增專案彈窗裡面的叉叉
        close_add_proj(){
            this.show_add_proj_type_list = false;
            this.proj_type_color = '#b6aeae';
            this.add_proj_type_text = '';
        },
  
        add_project(projName){
          const project = {
            name : projName,
            id: this.project_id, // 要跟後端拿
            type : this.proj_type,
            ended: false,
            trashcan: false
          }
  
          this.projects.push(project);
        },
  
        // find_project(project_name){
        //   // const proj_name = project_name;
        //   this.found_project = this.projects.find(project => 
        //     project.name === project_name
        //   );
        //   console.log({text:this.found_project.name});
        //   // console.log({text: this.found_project.name});
        // },
        // 新增專案彈窗裡點擊建立專案
        new_project_btn() {
            this.add_proj_show = this.add_proj_show === false ? true : false;
            this.showOverlay = false;
            this.middle_show_overview_page = true
            this.middle_show_over_page = false
            this.middle_show_trash_page = false
            this.selectOption = 'option1';
            this.show_add_proj_type_list = false;
            this.proj_type_color = '#b6aeae';
           
            if(this.add_proj_name !== ''){
                  if(this.proj_type === '選擇專案類型'|| this.proj_type === '未分類'){
                      this.add_project(this.add_proj_name);
                      this.uncategorized_projs.push(this.add_proj_name);
                      this.add_proj_name = '';
                  }
                  else if(this.add_proj_type_options.includes(this.proj_type) === true){
                      this.add_project(this.add_proj_name);
                      this.carts[this.add_proj_type_options.indexOf(this.proj_type)].project_box.push(this.add_proj_name);
                      this.add_proj_name = '';
                  }
                  else if(this.add_proj_type_options.includes(this.proj_type) === false){
                      const new_cart={
                          title_word: this.proj_type,
                          project_box: [this.add_proj_name],
                      }
                      this.carts.push(new_cart);
                      this.add_project(this.add_proj_name);
                      this.add_proj_type_options.push(new_cart.title_word)
                  }
              }
              this.add_proj_type_text = '';
              
          },
        // 左邊總攬、已結束、垃圾桶切換
        change(index) {
            if (index === 1) {
                this.middle_show_overview_page = true
                this.middle_show_over_page = false
                this.middle_show_trash_page = false
            }
            if (index === 2) {
                this.middle_show_over_page = true
                this.middle_show_overview_page = false
                this.middle_show_trash_page = false
                const info = {
                    user_id : 1,
                    project_status : 'ended',
                }
                axios.post(this.getPath,info).then(res => {
                    console.log(res.data.items);
                    this.ended_projects.push();
                    res.data.items["未分類"].forEach(project =>{
                        console.log(project.project_name);
                        this.ended_projects.push(project.project_name);
                    });
                })
            }
            if (index === 3) {
                this.middle_show_trash_page = true
                this.middle_show_overview_page = false
                this.middle_show_over_page = false
                const info = {
                    user_id : "1",
                    project_status : 'trashcan',
                }
                axios.post(this.getPath, info).then(res => {
                  console.log(res.data.item.in_month.map(project => project.project_name));
                  res.data.item.in_month.forEach(project => {
                        this.trash_boxes.push( { text: project.project_name } );
                    });
                })
            }
        },
        // 我忘了
        blurSelect() {
            this.$refs.select.blur();
        },
        // 滑鼠點擊新增專案的輸入框使其border變寬
        new_type_focus(){
            this.isFocused = true;
        },
        // 滑鼠離開新增專案的輸入框使其border還原
        new_type_blur(){
            this.isFocused = false;
            this.cart_title_input = '';
        },
        // 從新增專案的輸入框直接新增一個類型
        add_a_cart(){
            if(this.cart_title_input !== ''){
                const new_cart={
                    title_word: this.cart_title_input,
                    project_box: [],
                };
                this.carts.push(new_cart);
                this.add_proj_type_options.push(this.cart_title_input)
                this.cart_title_input = '';
            }
        },
        // 新增專案彈窗裡點擊選擇專案類型
        add_proj_type_btn(){
            this.show_add_proj_type_list = this.show_add_proj_type_list === false ? true : false;
            this.add_proj_type_arrow = 'url(../assets/dropdown_arrow/dropdown_arrow_down.svg) no-repeat center right;';
        },
        // 新增專案彈窗裡的選擇專案類型選擇其中一個已有專案
        type_choosen(option){
            this.show_add_proj_type_list = false;
            this.proj_type = option;
            this.proj_type_color = 'black';
            this.add_proj_type_text = '';
        },
        // 新增專案彈窗裡的選擇專案類型沒有選擇其中一個已有專案
        type_not_choose(){
            this.show_add_proj_type_list = false;
            this.proj_type = '未分類';
            this.proj_type_color = 'black';
            this.add_proj_type_text = '';
        },
        // 新增專案彈窗裡的選擇專案類型直接打字輸入新的專案
        list_add_a_cart(){
            if(this.add_proj_type_text !== ''){
                this.show_add_proj_type_list = false;
                this.proj_type = this.add_proj_type_text;
                this.proj_type_color = 'black';
                this.add_proj_type_text = '';
            }
        },
  
        //還沒有地方可以結束專案所以目前沒辦法加功能
        set_ended_project(){
          this.ended = true;
          const endPath = "http://localhost:5000/set_project_end";
          axios.post(endPath, this.project_id).then(res => {
            console.log(res.data.message);
          })
          const endParts = {
            tit : this.found_project.type,
            project_box : [ {text: this.found_project.name} ]
          }
  
          this.ended_projects.push(endParts);
        },
  
        //刪除後的專案跑到垃圾桶
        delete_project_click() {  //可以刪除總覽的project 但沒辦法拿到專案名稱
           // 請求獲取專案資料
            const trashPath = "http://35.194.196.179:5000/to_trashcan";
            axios.post(trashPath, this.project_id);
  
            console.log('刪除按鈕被點擊');
            this.close_delete_confirm();
            
            
        },
  
  
        // 點擊垃圾桶裡的專案後又上兩個按鈕變色
        selected_trash_box(index){
            const allFalse = this.checked_trash_box.every(function(element){
                return element === false
            })
            if (allFalse){
                this.recover = true;
                this.trashcan = true;
            }
            else{
                this.recover = false;
                this.trashcan = false;
            }
        },
        // 垃圾桶點擊還原專案
        recover_project(){
            //獲得專案資料
            
            this.recovered = true;
            setTimeout(() => {
                this.recovered = false;
            }, 1000);
            this.recover = true;
            this.trashcan = true;
  
            const recoverPath = "http://localhost:5000/trashcan_recover";
            axios.post(recoverPath, this.project_id);
            
        },
        // 垃圾桶點選永久刪除
        forever_delete_project(){ 
            this.forever_delete_confirm = true;
            this.showOverlay_trash = true;
        },
  
        forever_delete_project_delete(){
          const trashIdx = this.trash_boxes.indexOf(this.found_project.name);
          console.log(this.found_project.name);
          this.close_forever_delete_confirm();
          this.trash_boxes.splice(trashIdx,1);
          // this.trash_boxes = this.trash_boxes.filter(trashbox => trashbox.name !== this.found_project.name);
        },
        // 關閉永久刪除彈窗
        close_forever_delete_confirm(){
            this.forever_delete_confirm =false;
            this.showOverlay_trash = false;
        },
        // 專案總覽右鍵點擊專案
        right_click_box(event){
            event.preventDefault();
            this.right_click_box_overview_show = true;
            this.mouseTop = event.clientY - 49;
            this.mouseLeft = event.clientX - 368;
        },
        // 當滑鼠點擊非指定區域時關閉彈窗
        handleClickOutside(){
            // 專案總覽右鍵彈窗
            if(this.right_click_box_overview_show === true && !this.$refs.right_click_box_overview.contains(event.target) && this.showOverlay_delete === false){
                this.right_click_box_overview_show = false
            }
            // 新增專案彈窗裡的選擇新增專案類型彈窗
            else if(this.show_add_proj_type_list === true && !this.$refs.add_proj_type_list.contains(event.target)){
                if(!this.$refs.add_proj_type.contains(event.target)){
                    this.show_add_proj_type_list = false;
                    this.add_proj_type_text = '';
                }
            }
            else if(this.right_click_box_trash_show === true && !this.$refs.right_click_box_trash.contains(event.target) && this.showOverlay_trash === false){
                this.right_click_box_trash_show = false
            }
        },
        // 專案總覽右鍵選擇刪除專案
        delete_project(){
            this.delete_confirm = true;
            this.showOverlay_delete = true;
        },
        // 關閉刪除按鈕彈窗
        close_delete_confirm(){
            this.delete_confirm = false;
            this.showOverlay_delete = false;
        },
        // 垃圾桶右鍵點擊專案
        right_click_box_trash(event){
            event.preventDefault();
            this.right_click_box_trash_show = true;
            this.mouseTop = event.clientY - 49;
            this.mouseLeft = event.clientX - 368;
        },
    },
    mounted() {
        window.addEventListener('click' , this.handleClickOutside);
    },
    beforeUnmount() {
        window.removeEventListener('click', this.handleClickOutside);
    },
  }
  </script>
  
  <style scoped>
  * {
    margin: 0;
    padding: 0;
    font-family: 'Noto Sans TC';
  }
  
  /* navigation bar的部分 起點*/
  .nav {
    width: 100vw;
  
    height:calc(49px * 0.9);
    background-color: white;
    box-shadow: 0px 4px 4px rgba(0, 0, 0, 0.25);
    position: fixed;
    z-index: 9;
  }
  
  .nav>img {
    height: 32.06px;
    width: auto;
    position: absolute;
    top: 8px;
    left: 2.6%;
    -webkit-user-drag: none;
    user-select: none;
  }
  
  .tri_btn {
    width: 340px;
    height: 30px;
    
    position: absolute;
    right: 50px;
    top: 9.03px;
  }
  
  .tri_btn input {
    width: 248px;
    height: 25.2px;
    background-color: #f2eeee;
    border-radius: 24px;
    border: 1px solid transparent;
    outline: none;
    text-indent: 43px;
    font-size: 16px;
    font-weight: 400;
    position: absolute;
  }
  
  
  .tri_btn input:hover {
    background-color: #e1dcdc;
  }
  
  .tri_btn input:focus {
    background-color: white;
    border-color: #c7c2c2;
  }
  
  .search {
    position: absolute;
    top: 7px;
    left: 15px;
    -webkit-user-drag: none;
    user-select: none;
  }
  
  .notice {
    position: absolute;
    right: 45px;
    cursor: pointer;
    -webkit-user-drag: none;
    user-select: none;
  }
  
  .notice:hover {
    content: url(../assets/Notice/Notice_Hover.svg);
  }
  
  .notice:active {
    content: url(../assets/Notice/Notice_Active.svg);
  }
  
  .profile {
    position: absolute;
    right: 0px;
    cursor: pointer;
    -webkit-user-drag: none;
    user-select: none;
  }
  
  .profile:hover {
    content: url(../assets/Profile/Profile_Hover.svg);
  }
  
  .profile:active {
    content: url(../assets/Profile/Profile_Active.svg);
  }
  
  /* navigation bar的部分 終點 */
  
  /* 左側欄的部分 起點 */
  .left_bar {
    width: 260px;
    /* width: calc(260px * 0.9); */
    height: calc(100vh - 48px);
  
    background-color: #f2eeee;
    border-radius: 0px 14px 14px 0px;
    box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.25);
    position: fixed;
    bottom: 0px;
    z-index: 8;
  }
  
  .add_btn {
    width: 170px;
    height: 65px;
    /* width: calc(170px * 0.9);
    height: calc(65px * 0.9);  */
  position: relative;
  top: 40px;
  left: 48px;
  border-radius: 32px;
  box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.4);
  background-color: #b82c30;
  cursor: pointer;
  font-size: 18px;
  font-weight: 500;
  letter-spacing: 1.25px;
  line-height: 65px;
  color: white;
  text-indent: 68px;
  user-select: none;
}

.plus {
  position: relative;
  width: 14px;
  height: 14px;
  background-color: transparent;
  border: 1.5px solid transparent;
}

.plus::before,
.plus::after {
  content: "";
  position: absolute;
  width: 100%;
  height: 1.5px;
  background-color: white;
  top: 50%;
  left: 83px;
}

.plus::before {
  transform: rotate(90deg);
}

.plus::after {
  transform: rotate(0deg);
}

.three_pointer {
  width: 100%;
  height: 228px;
  position: relative;
  top: 61px;
}

.three_pointer input[type="radio"] {
  display: none;
}

.three_pointer input[type="radio"] + label {
  display: inline-block;
  width: 100%;
  height: 76px;
  background-color: transparent;
  font-size: 19px;
  font-weight: 400;
  line-height: 76px;
  letter-spacing: 0.15px;
  text-indent: 116px;
  cursor: pointer;
  user-select: none;
}

.three_pointer input[type="radio"]:hover + label {
  background-color: #e1dcdc;
}

.three_pointer input[type="radio"]:checked + label {
  background-color: #e1dcdc;
}

.three_pointer img {
  position: absolute;
  left: 64px;
  -webkit-user-drag: none;
  user-select: none;
  cursor: pointer;
}

/* 左側欄的部分 終點 */

/* 新增專案的框框 起點 */
.add_proj_box {
  width: 344px;
  height: 524px;
  /* width: calc(344px * 0.9);
    height: calc(524px * 0.9); */
  position: fixed;
  border-radius: 14px;
  background-color: white;
  box-shadow: 0px 8px 12px rgba(0, 0, 0, 0.4);
  /* top: 244px;
    left: 924px; */
  z-index: 6;
  left: calc((100vw - 344px + 234px) / 2);
  top: calc((100vh - 524px + 50px) / 2);
}

.close_add_proj_box {
  position: relative;
  width: 12px;
  height: 12px;
  cursor: pointer;
  top: 25px;
  left: 307px;
}

.close_add_proj_box::before,
.close_add_proj_box::after {
  content: "";
  position: absolute;
  top: 50%;
  left: 50%;
  width: 2px;
  height: 17px;
  background-color: black;
}

.close_add_proj_box::before {
  transform: translate(-50%, -50%) rotate(45deg);
}

.close_add_proj_box::after {
  transform: translate(-50%, -50%) rotate(-45deg);
}

.add_proj_title {
  font-size: 20px;
  font-weight: 600;
  position: relative;
  top: 20px;
  text-align: center;
  user-select: none;
}

.add_proj_pic {
  width: 280px;
  height: 140px;
  border-radius: 14px;
  background-color: #f2eeee;
  position: relative;
  top: 60px;
  left: 50%;
  transform: translate(-50%);
  cursor: pointer;
  -webkit-user-drag: none;
}

.add_proj_pic_plus {
  position: relative;
  top: 40px;
  left: 110px;
  user-select: none;
  -webkit-user-drag: none;
}

.add_proj_name {
  width: 278px;
  height: 38px;
  border: 1px solid #c7c2c2;
  border-radius: 12px;
  font-size: 16px;
  letter-spacing: 1.25px;
  line-height: 38px;
  text-indent: 20px;
  position: relative;
  top: 108px;
  left: 50%;
  transform: translate(-50%);
}

.add_proj_name:hover {
  border-color: #b6aeae;
}

.add_proj_name:focus {
  border-color: #3b3838;
  outline: #7b7b7b;
}

.add_proj_name::placeholder {
  user-select: none;
  color: #b6aeae;
}

.add_proj_type {
  width: 278px;
  height: 38px;
  border: 1px solid #b8b8b8;
  border-radius: 12px;
  position: relative;
  top: 124px;
  left: 50%;
  transform: translate(-50%);
  font-size: 16px;
  letter-spacing: 1.25px;
  line-height: 36px;
  text-indent: 20px;
  color: #b6aeae;
  cursor: pointer;
  user-select: none;
  -webkit-appearance: none;
  -moz-appearance: none;
  appearance: none;
  background: url(../assets/dropdown_arrow/dropdown_arrow_right.svg) no-repeat
    center right;
}
.add_proj_type:hover {
  border-color: #7b7b7b;
  background: url(../assets/dropdown_arrow/dropdown_arrow_right_hover.svg)
    no-repeat center right;
}

.add_proj_type_list {
  width: 214px;
  height: auto;
  padding-top: 8px;
  box-shadow: 0px 1px 2px rgba(0, 0, 0, 0.3), 0px 2px 15px rgba(0, 0, 0, 0.15);
  border-radius: 14px;
  position: absolute;
  top: 396px;
  left: 86px;
  z-index: 3;
  background-color: white;
}
.add_proj_type_option {
  width: 100%;
  height: 45px;
  line-height: 45px;
  font-size: 16px;
  font-weight: 500;
  letter-spacing: 1.25;
  text-indent: 16px;
  cursor: pointer;
  color: #3b3838;
  user-select: none;
}
.add_proj_type_option:hover {
  background-color: #f2eeee;
}
.add_proj_type_list_line {
  height: 7px;
  border-bottom: 2px solid #e1dcdc;
  margin-bottom: 7px;
  user-select: none;
}
.add_proj_type_text {
  height: 45px;
  width: 100%;
  font-size: 16px;
  font-weight: 500;
  letter-spacing: 1.25;
  text-indent: 16px;
  border: none;
  outline: none;
  color: #3b3838;
  user-select: none;
}
.add_proj_type_text::placeholder {
  color: #3b3838;
}
.add_proj_type_text:hover {
  background-color: #f2eeee;
}
.add_proj_type_text_plus {
  position: relative;
  width: 9.33px;
  height: 9.33px;
  background-color: transparent;
  border: 1px solid transparent;
  top: -23px;
}

.add_proj_type_text_plus::before,
.add_proj_type_text_plus::after {
  content: "";
  position: absolute;
  width: 100%;
  height: 1px;
  background-color: #120405;
  top: 0px;
  left: 176.83px;
  -webkit-user-drag: none;
  cursor: pointer;
}

.add_proj_type_text_plus::before {
  transform: rotate(90deg);
}

.add_proj_type_text_plus::after {
  transform: rotate(0deg);
}

.add_proj_build {
  width: 280px;
  height: 48px;
  border-radius: 14px;
  background-color: #b82c30;
  color: white;
  font-size: 18px;
  font-weight: 500;
  line-height: 48px;
  letter-spacing: 1.25px;
  text-align: center;
  position: relative;
  top: 170px;
  left: 50%;
  transform: translate(-50%);
  cursor: pointer;
  user-select: none;
}

/* 新增專案的框框 終點 */

/* 背景灰色 */
.overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(59, 56, 56, 0.5);
  z-index: 5;
}

/* 中間的部分 起點 */
.bg {
  width: calc(100vw - 272px);
  height: calc(100vh - 48px);
  position: fixed;
  bottom: 0px;
  right: 12px;
  background-image: url(../assets/bricks_bg_small.svg);
  overflow-x: auto;
  overflow-y: hidden;
}

.middle {
  width: 94%;
  height: calc(90vh - 20.3px);
  /* height: 500px; */
  position: absolute;
  overflow-y: auto;
  overflow-x: hidden;
  top: 0px;
  left: 75px;
  align-items: center;
  padding-bottom: 20px;
}

::-webkit-scrollbar {
  display: none;
}
.cart {
  width: calc(100% - 50px);
  min-height: 218px;
  background-color: white;
  border-radius: 14px;
  border: 1px solid #e1dcdc;
  box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);
  margin-bottom: 20px;
}

.uncategorized {
  margin-top: 60px;
  background-color: #f2eeee;
  display: inline-block;
}

.cart_title {
  font-size: 16px;
  font-weight: 400;
  line-height: 24px;
  height: 24px;
  letter-spacing: 0.5px;
  position: relative;
  top: 22px;
  left: 96px;
  /* display: inline-block; */
}
.cart_drag_icon {
  position: relative;
  -webkit-user-drag: none;
  user-select: none;
  top: 22px;
  left: 32px;
  display: inline-block;
}
.title_underline {
  width: 304px;
  border-bottom: 1px solid #c7c2c2;
  position: relative;
  top: 30px;
  left: 80px;
}

.box_container {
  width: 100%;
  height: auto;
  position: relative;
  top: 56px;
  left: 80px;
  overflow: hidden;
  margin-bottom: 80px;
}

.box_container .box {
  width: 295px;
  /* 希望box可以隨著container等比例縮放 */

  height: 44px;
  border: 1.5px solid #e1dcdc;
  border-radius: 13px;
  background-color: white;
  float: left;
  margin: 0 16px 13px 0;
  cursor: pointer;
  font-size: 16px;
  line-height: 44px;
  font-weight: 400;
  letter-spacing: 1.25px;
  text-indent: 69.67px;
  user-select: none;
}
.box:hover {
  background-color: #e1dcdc;
  border-color: #c7c2c2;
}
.cart_title_input {
  font-size: 16px;
  font-weight: 400;
  line-height: 24px;
  letter-spacing: 0.5px;
  position: relative;
  top: 22px;
  left: 96px;
  border: none;
  outline: none;
}
.new_type_highlight {
  border: 2px solid #c7c2c2;
}
.right_click_box_overview {
  width: 214px;
  height: 106px;
  box-shadow: 0px 1px 2px rgba(0, 0, 0, 0.3), 0px 2px 15px rgba(0, 0, 0, 0.15);
  border-radius: 14px;
  background-color: white;
  padding-top: 8px;
  padding-bottom: 8px;
  position: absolute;
}
.right_click_box_overview_option {
  width: 100%;
  height: 45px;
  font-size: 16px;
  line-height: 45px;
  letter-spacing: 1.25px;
  color: rgba(59, 56, 56, 1);
  font-weight: 500;
  text-indent: 16px;
  user-select: none;
  cursor: pointer;
}
.right_click_box_overview_option:hover {
  background-color: #f2eeee;
}
.delete_confirm {
  width: 412px;
  height: 372px;
  position: absolute;
  top: 20%;
  left: 520px;
  background-color: white;
  border: 1.5px solid #c7c2c2;
  box-shadow: 0px 0px 5px 1px rgba(65, 65, 65, 0.25);
  border-radius: 14px;
  z-index: 8;
}
.delete_confirm_first_text {
  width: 104px;
  height: 28px;
  position: relative;
  top: 28px;
  left: 50%;
  transform: translate(-50%);
  font-size: 26px;
  font-weight: 700;
  line-height: 28px;
  user-select: none;
}
.close_delete_confirm {
  position: relative;
  width: 12px;
  height: 12px;
  cursor: pointer;
  top: 25px;
  left: 375px;
}

.close_delete_confirm::before,
.close_delete_confirm::after {
  content: "";
  position: absolute;
  top: 50%;
  left: 50%;
  width: 1.5px;
  height: 17px;
  background-color: black;
}

.close_delete_confirm::before {
  transform: translate(-50%, -50%) rotate(45deg);
}

.close_delete_confirm::after {
  transform: translate(-50%, -50%) rotate(-45deg);
}
.delete_confirm img {
  -webkit-user-drag: none;
  user-select: none;
  position: relative;
  top: 56px;
  left: 50%;
  transform: translate(-50%);
}
.delete_confirm_second_text {
  position: relative;
  color: #3b3838;
  font-weight: 400;
  font-size: 14px;
  height: 21px;
  line-height: 21px;
  letter-spacing: 0.25px;
  user-select: none;
  top: 83px;
  left: 50%;
  transform: translate(-50%);
  width: 100px;
}
.delete_confirm_third_text {
  position: relative;
  color: #3b3838;
  font-weight: 400;
  font-size: 14px;
  height: 21px;
  line-height: 21px;
  letter-spacing: 0.25px;
  user-select: none;
  top: 83px;
  left: 50%;
  transform: translate(-50%);
  width: 243px;
}
.delete_confirm_btn_container {
  width: 332px;
  height: 48px;
  position: relative;
  top: 108px;
  left: 50%;
  transform: translate(-50%);
}
.forever_delete_confirm_btn {
  width: 150px;
  height: 48px;
  border-radius: 14px;
  cursor: pointer;
  background-color: #b82c30;
  color: white;
  font-size: 18px;
  letter-spacing: 1.25px;
  font-weight: 500;
  line-height: 48px;
  border: none;
  float: right;
  user-select: none;
}
.forever_delete_confirm_btn_cancel {
  background-color: white;
  color: #120405;
  float: left !important;
}
/* 中間的部分 終點 */

/* 垃圾桶的部分 起點 */
.trash_page_middle {
  width: 99%;
  height: 85vh;
  border: 1px solid #e1dcdc;
  box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);
  border-radius: 14px;
  background-color: white;
  margin-top: 40px;
}
.last_30_days {
  width: 1264px;
  min-height: 222px;
  margin-top: 40px;
  position: relative;
  left: 80px;
  padding-bottom: 25px;
}
.last_time {
  position: relative;
  height: 44px;
  left: 16px;
  color: #3b3838;
  font-size: 16px;
  letter-spacing: 0.5px;
  line-height: 44px;
  user-select: none;
}
.time_subline {
  width: 304px;
  height: 1px;
  border-bottom: 1px solid #c7c2c2;
  position: relative;
}
.trash_pic {
  -webkit-user-drag: none;
  user-select: none;
}
.recover {
  position: absolute;
  top: 0px;
  right: 68px;
}
.forever_delete {
  position: absolute;
  top: 0px;
  right: 0px;
}
.trash_box_container {
  width: 1280px;
  height: auto;
  position: relative;
  top: -10px;
  overflow: hidden;
  margin-bottom: 0px;
}
.trash_box input[type="checkbox"] {
  display: none;
}
.trash_box input[type="checkbox"] + label {
  width: 301px;
  height: 44px;
  border: 1.5px solid #e1dcdc;
  border-radius: 13px;
  background-color: white;
  float: left;
  margin: 0 16px 25px 0;
  cursor: pointer;
  font-size: 16px;
  line-height: 44px;
  font-weight: 400;
  letter-spacing: 1.25px;
  text-indent: 69.67px;
  user-select: none;
}
.trash_box input[type="checkbox"]:hover + label {
  background-color: #f2eeee;
}
.trash_box input[type="checkbox"]:active + label {
  background-color: #f2eeee;
}
.trash_box input[type="checkbox"]:checked + label {
  background-color: #f2eeee;
}
.last_one_year {
  width: 1264px;
  min-height: 242px;
  position: relative;
  top: 50px;
  left: 80px;
}
.recovered {
  width: 399px;
  height: 141px;
  background-color: white;
  box-shadow: 0px 8px 12px rgba(0, 0, 0, 0.4);
  border-radius: 14px;
  position: absolute;
  top: 30vh;
  left: 529px;
  z-index: 9;
}
.recovered img {
  position: relative;
  top: 32px;
  left: 183.5px;
  -webkit-user-drag: none;
  user-select: none;
}
.recovered p {
  position: relative;
  top: 40px;
  left: 164px;
  font-size: 14px;
  font-weight: 400;
  letter-spacing: 0.25px;
  color: #3b3838;
  user-select: none;
  -webkit-user-drag: none;
}
.forever_delete_confirm {
  width: 412px;
  height: 372px;
  position: absolute;
  top: 20%;
  left: 520px;
  background-color: white;
  border: 1.5px solid #c7c2c2;
  box-shadow: 0px 0px 5px 1px rgba(65, 65, 65, 0.25);
  border-radius: 14px;
  z-index: 8;
}
.forever_delete_confirm_first_text {
  width: 156px;
  height: 28px;
  position: relative;
  top: 28px;
  left: 50%;
  transform: translate(-50%);
  font-size: 26px;
  font-weight: 700;
  line-height: 28px;
  user-select: none;
}
.close_forever_delete_confirm {
  position: relative;
  width: 12px;
  height: 12px;
  cursor: pointer;
  top: 25px;
  left: 375px;
}

.close_forever_delete_confirm::before,
.close_forever_delete_confirm::after {
  content: "";
  position: absolute;
  top: 50%;
  left: 50%;
  width: 1.5px;
  height: 17px;
  background-color: black;
}

.close_forever_delete_confirm::before {
  transform: translate(-50%, -50%) rotate(45deg);
}

.close_forever_delete_confirm::after {
  transform: translate(-50%, -50%) rotate(-45deg);
}
.forever_delete_confirm img {
  -webkit-user-drag: none;
  user-select: none;
  position: relative;
  top: 56px;
  left: 50%;
  transform: translate(-50%);
}
.forever_delete_confirm_second_text {
  position: relative;
  color: #3b3838;
  font-weight: 400;
  font-size: 14px;
  height: 21px;
  line-height: 21px;
  letter-spacing: 0.25px;
  user-select: none;
  top: 83px;
  left: 50%;
  transform: translate(-50%);
  width: 243px;
}
.forever_delete_confirm_btn_container {
  width: 332px;
  height: 48px;
  position: relative;
  top: 108px;
  left: 50%;
  transform: translate(-50%);
}
.forever_delete_confirm_btn {
  width: 150px;
  height: 48px;
  border-radius: 14px;
  cursor: pointer;
  background-color: #b82c30;
  color: white;
  font-size: 18px;
  letter-spacing: 1.25px;
  font-weight: 500;
  line-height: 48px;
  border: none;
  float: right;
  user-select: none;
}
.forever_delete_confirm_btn_cancel {
  background-color: white;
  color: #120405;
  float: left !important;
}
.recover_trash_pic {
  width: auto;
  height: auto;
  position: relative;
  left: 1125px;
  bottom: 45px;
}

/* 垃圾桶的部分 終點 */
</style>
