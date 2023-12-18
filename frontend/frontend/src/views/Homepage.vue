<template>
  <div style="width: 100%; position: absolute; left: 0; top: 0">
    <div class="nav" v-if="scroll" style="background-color: transparent">
      <a href="./homepage_2">
        <img src="../assets/brickslogo.svg" alt="" />
      </a>

      <div class="tribtn">
        <div class="btn">試用</div>
        <a href="./login" class="btn nav_login_btn">登入</a>
        <a href="./register" class="btn" style="margin-right: 0px">註冊</a>
      </div>
    </div>
    <div class="nav_scroll" v-else style="background-color: white">
      <a href="./homepage_2">
        <img src="../assets/brickslogo.svg" alt="" />
      </a>
      <div class="tribtn">
        <div class="btn">試用</div>
        <a
          href="./login_2"
          class="btn nav_login_btn"
          style="
            background-color: #b82c30;
            border-color: #b82c30;
            color: #ffffff;
          "
          >登入</a
        >
        <a href="./register_2" class="btn" style="margin-right: 0px">註冊</a>
      </div>
    </div>
    <div class="first_bg">
      <div class="slogan">
        <div class="first_line">
          <p style="float: left">一磚一磚</p>
          <p style="float: right">
            建<span style="letter-spacing: 0">造</span>
          </p>
        </div>
        <p class="second_line">
          你的專<span style="letter-spacing: 0">案</span>
        </p>
        <p class="third_line">
          為大學生設計的專案管理工<span style="letter-spacing: 0">具</span>
        </p>
        <a href="" class="try_now_first">立即試用</a>
      </div>
    </div>
    <div class="sec_body">
      <div class="card">
        <img src="../assets/screen_shot.png" alt="" />
        <div class="text_area first_text_area">
          <p class="line_one"># 輕鬆開會</p>
          <p class="line_two">最方便的會議紀錄</p>
          <p class="three_adv">
            # 利用 Hashtag 標籤，快速搜尋過往內容<br />
            # 建立自訂的範本，不再需要每次重開<br />
            # 封存先前的紀錄，避免不慎更動
          </p>
          <a href="" class="mid_try_btn">立即試用</a>
        </div>
        <div class="cover"></div>
      </div>
      <div class="card sec_card">
        <img src="../assets/screen_shot.png" alt="" />
        <div class="text_area">
          <p class="line_one"># 層級分明</p>
          <p class="line_two">繪製組織架構圖</p>
          <p class="three_adv">
            # 圖像化的架構，組織層級一目瞭然<br />
            # 依照層級賦予權限<br />
            # 可隨時更改，應付各種人員流動
          </p>
        </div>
        <div class="cover"></div>
      </div>
      <div class="card">
        <img src="../assets/screen_shot.png" alt="" />
        <div class="cover"></div>
        <div class="text_area">
          <p class="line_one"># 創意發想</p>
          <p class="line_two">隨時隨地 IG 式提案</p>
          <p class="three_adv">
            # 隨時隨地向眾人發表提案<br />
            # 類 IG 的操作介面<br />
            # 投票、抽籤等多功能匯總
          </p>
        </div>
      </div>
      <div class="last_text_area">
        <p class="end_first_line">
          比 Google 文件更方便<br />
          比 Notion 更直覺
        </p>
        <p class="end_sec_area">
          周全不繁瑣的會議功能<br />
          簡單易上手的操作介面<br />
          現在就用 <span style="color: #b82c30">BRICKS</span> 完善你的專案！
        </p>
        <a href="" class="end_try_btn">立即試用</a>
      </div>
    </div>

    <div class="bottom">
      <a href="" class="privacy"
        ># <span style="text-decoration: underline">隱私權政策</span></a
      >
      <a href="" class="contact"
        ># 聯絡我們 <span style="color: #b6aeae">bricks@gmail.com</span></a
      >
      <div class="photo">
        # Photo by
        <a href="https://unsplash.com/@charlesdeluvio">charlesdeluvio</a> on
        Unsplash
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "Homepage",
  data() {
    return {
      scroll: true,
    };
  },
  methods: {
    handleScroll() {
      var top = Math.floor(document.documentElement.scrollTop);
      var screenHeight = window.innerHeight;
      var threshold = screenHeight * 1; // 將螢幕高度乘上1，即為100%的高度

      if (top > threshold) {
        this.scroll = false;
      } else {
        this.scroll = true;
      }
    },
  },
  created() {},
  mounted() {
    window.addEventListener("scroll", this.handleScroll);
  },
};
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
  font-family: "PingFang SC", "Helvetica Neue";
  box-sizing: border-box;
}

.nav {
  width: 100%;
  height: 65px;
  position: fixed;
  z-index: 100;
}

.nav_scroll {
  width: 100%;
  height: 65px;
  box-shadow: 0px 4px 4px rgba(0, 0, 0, 0.25);
  position: fixed;
  z-index: 9;
}

.nav img {
  height: 32.06px;
  width: auto;
  position: absolute;
  top: 16.47px;
  left: 5.21%;
}

.nav_scroll img {
  height: 32.06px;
  width: auto;
  position: absolute;
  top: 16.47px;
  left: 5.21%;
}

.tribtn {
  width: 284px;
  height: 41px;
  position: absolute;
  top: 12px;
  right: 5.21%;
}

.btn {
  width: 76px;
  height: 39px;
  border: 1px solid #120405;
  background-color: transparent;
  border-radius: 10px;
  float: left;
  margin-right: 25px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  line-height: 39px;
  font-family: "Noto Sans TC";
  text-align: center;
  letter-spacing: 1.25px;
  user-select: none;
  text-decoration: none;
  color: black;
}

.btn:hover {
  background-color: rgba(242, 238, 238, 1);
}

.nav_login_btn {
  background-color: #b82c30;
  border-color: #b82c30;
  color: #ffffff;
}

.nav_login_btn:hover {
  background-color: rgba(212, 128, 131, 1);
}

.first_bg {
  background-image: url(../assets/homepage_bg.svg);
  width: 100%;
  height: 100vh;
  background-size: cover;
  /* background-position: top; */
  position: relative;
}

.slogan {
  width: 70%;
  height: 368px;
  position: relative;
  left: 50%;
  transform: translate(-50%);
  top: 28vh;
  font-family: "Noto Sans TC";
}

.first_line {
  font-size: 3.5vw;
  font-weight: 400;
  height: 56.4px;
  width: 40%;
  line-height: 56.4px;
  position: absolute;
  left: 50%;
  transform: translate(-50%);
  letter-spacing: 12px;
  top: 0px;
}

.second_line {
  font-size: 6vw;
  font-weight: 700;
  line-height: 112px;
  position: absolute;
  left: 50%;
  display: flex;

  transform: translate(-50%);
  letter-spacing: 24px;
  top: 4vw;
}

.third_line {
  font-size: 2.2vw;
  font-weight: 400;
  height: 40px;
  width: auto;
  line-height: 40px;
  position: absolute;
  left: 50%;
  transform: translate(-50%);
  letter-spacing: 0.25px;
  top: 14vw;
  /* border: #120405 2px solid; */
}

.try_now_first {
  width: 272px;
  height: 48px;
  background-color: #b82c30;
  border-radius: 14px;
  position: absolute;
  bottom: 5vh;
  left: 50%;
  transform: translate(-50%);
  text-decoration: none;
  font-size: 18px;
  font-weight: 500;
  color: white;
  line-height: 48px;
  text-align: center;
  letter-spacing: 4px;
}

.try_now_first:hover {
  background-color: #d48083;
}

.try_now_first:active {
  background-color: #932326;
}

.sec_body {
  width: 100%;
  height: 170vw;
  background-image: url(../assets/bricks_bg.svg);
  background-size: cover;
}

.card {
  width: 86vw;
  height: 36vw;
  position: relative;
  left: 50%;
  transform: translate(-50%);
  top: 16vh;
  margin-bottom: 8vh;
}

.card img {
  width: 60%;
  height: auto;
  aspect-ratio: 16/9;
  float: right;
  box-shadow: 0px 8px 12px rgba(0, 0, 0, 0.4);
  position: relative;
  top: 50%;
  transform: translate(0, -50%);
  right: 0;
}

@media screen and (max-width: 1024px) {
  .first_line {
    width: 44%;
  }
  .sec_body {
    height: 220vw;
  }
  .card {
    width: 70vw;
    height: auto;
    aspect-ratio: 16/9;
    position: relative;
    left: 50%;
    transform: translate(-50%);
    top: 16vh;
    margin-bottom: 12vh;
  }
  .card img {
    width: 100%;
    height: auto;
    position: absolute;
    left: 50%;
    transform: translateX(-50%);
    top: 0%;
    z-index: -1;
  }
  .sec_card img {
    float: none;
    transform: translateX(-4%);
  }
  .text_area {
    width: auto;
    height: 232px;
    position: relative;
    top: 10%;
    transform: none;
    left: 0;
    margin-left: 8%;
    z-index: 8;
  }
  .sec_card .text_area {
    margin-right: 8%;
  }
  .card .cover {
    background-color: rgba(0, 0, 0, 0.5);
    z-index: 2;
    width: 100%;
    height: auto;
    aspect-ratio: 16/9;
    position: absolute;
    left: 50%;
    transform: translateX(-50%);
    top: 0%;
    opacity: 0;
    transition: opacity 0.3s ease;
  }
  .card:hover .cover {
    opacity: 1;
  }

  .text_area .line_one {
    opacity: 0;
    color: #f3f3f3d8;
  }

  .text_area .line_two {
    opacity: 0;
    color: #f3f3f3;
    top: 0.5vh;
  }

  .text_area .three_adv {
    opacity: 0;
    color: #f3f3f3;
    top: 0.5vh;
  }
  .text_area .mid_try_btn {
    opacity: 0;
    /* border-bottom: 20%; */
  }
  .card:hover .text_area .line_one {
    opacity: 1;
  }

  .card:hover .text_area .line_two {
    opacity: 1;
  }

  .card:hover .text_area .three_adv {
    opacity: 1;
  }
  .card:hover .text_area .mid_try_btn {
    opacity: 0.8;
  }
  .try_now_first {
    bottom: 14vh;
  }
  .card .text_area {
    width: auto;
    height: 232px;
    position: relative;
    top: 50%;
    transform: translate(0, -34%);
    left: 0;
  }
  .card .first_text_area {
    top: 10vw;
    transform: translate(0, -10%);
    height: 80%;
  }
  .first_text_area .mid_try_btn {
    height: 15%;
    width: 30%;
    position: absolute;
    top: 65%;
    left: 0;
    font-size: 2.5vw;
    line-height: 4vw;
    letter-spacing: 1.25px;
    background-color: #b82c30;
    color: white;
  }
}

.sec_card img {
  float: left;
  left: 4%;
}

.sec_card .text_area {
  right: 0;
  float: right;
}

.text_area {
  width: auto;
  height: 232px;
  position: relative;
  top: 50%;
  transform: translate(0, -50%);
  left: 0;
}

.first_text_area {
  top: 68px;
  transform: none;
}

.line_one {
  height: 28px;
  line-height: 28px;
  color: #b6aeae;
  font-size: 2vw;
  font-weight: 700;
}

.line_two {
  height: 56px;
  line-height: 56px;
  color: #252525;
  font-size: 3.2vw;
  font-weight: 700;
}

.three_adv {
  position: relative;
  top: 5vh;
  height: 100px;
  color: #252525;
  font-size: 1.6vw;
  font-weight: 400;
}

.mid_try_btn {
  display: inline-block;
  color: #b82c30;
  height: 46px;
  width: 270px;
  border: 1px solid #b82c30;
  border-radius: 14px;
  background-color: white;
  position: relative;
  top: 10vh;
  left: 0;
  text-decoration: none;
  font-size: 18px;
  line-height: 46px;
  text-align: center;
  letter-spacing: 1.25px;
}

.mid_try_btn:hover {
  background-color: #f2eeee;
}

.mid_try_btn:active {
  background-color: #f1d5d6;
}

.last_text_area {
  width: 40vw;
  height: 30vw;
  position: relative;
  left: 50%;
  transform: translate(-50%);
  top: 24vh;
}

.end_first_line {
  font-size: 3.5vw;
  height: 56px;
  line-height: 56px;
  font-weight: 700;
  text-align: center;
}

.end_sec_area {
  font-size: 1.8vw;
  font-weight: 400;
  text-align: center;
  position: relative;
  top: 104px;
}

.end_try_btn {
  display: inline-block;
  width: 272px;
  height: 48px;
  border-radius: 14px;
  background-color: #b82c30;
  color: white;
  letter-spacing: 4px;
  position: relative;
  top: 160px;
  left: 28%;
  transform: translate(-50%);
  text-decoration: none;
  line-height: 48px;
  font-size: 18px;
  text-align: center;
}

.end_try_btn:hover {
  background-color: #d48083;
}

.end_try_btn:active {
  background-color: #932326;
}

.bottom {
  width: 100%;
  height: 65px;
  top: 0px;
  box-shadow: 0px -4px 8px rgba(0, 0, 0, 0.1);
  background-color: white;
  position: relative;
}

.privacy {
  width: 116px;
  height: 23px;
  font-size: 19px;
  font-family: "Noto Sans TC";
  line-height: 23px;
  position: absolute;
  top: 50%;
  transform: translate(0, -50%);
  letter-spacing: 0.15px;
  cursor: pointer;
  color: #120406;
  text-decoration: none;
}

.contact {
  width: 271px;
  height: 23px;
  font-size: 19px;
  font-family: "Noto Sans TC";
  line-height: 23px;
  position: absolute;
  top: 50%;
  transform: translate(0, -50%);
  letter-spacing: 0.15px;
  cursor: pointer;
  color: #120406;
  text-decoration: none;
}

.photo {
  width: 357px;
  height: 23px;
  font-size: 19px;
  font-family: "Noto Sans TC";
  line-height: 23px;
  position: absolute;
  top: 50%;
  transform: translate(0, -50%);
  letter-spacing: 0.15px;
  color: #c7c2c2;
}

.photo a {
  color: #c7c2c2;
}

.privacy {
  left: 540px;
}

.contact {
  left: 688px;
}

.photo {
  right: 540px;
}
</style>
