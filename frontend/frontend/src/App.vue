<template>
  <!-- <nav>
    <router-link to="/">Home</router-link> |
    <router-link to="/about">About</router-link> |
    <router-link to="/tim">Tim</router-link> |
    <router-link to="/karen">Karen</router-link> |
    <router-link to="/sharon">Sharon</router-link> |
    <router-link to="/kerwin">Kerwin</router-link>
  </nav> -->

  <!-- 加上這個才會顯示 views 裏面的東西 -->
  <router-view />
</template>

<script>
export default {
  components: {},
  setup() {
    return {};
  },
};
</script>

<style>
#app {
  font-family: 'PingFang TC', 'Helvetica Neue';
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

nav {
  padding: 30px;
}

nav a {
  font-weight: bold;
  color: #2c3e50;
}

nav a.router-link-exact-active {
  color: #c91f2f;
}

#app {
  margin: 0;
  padding: 0;
  border: 0;
}
</style>
