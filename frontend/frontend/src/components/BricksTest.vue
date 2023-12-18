<template>
  <div>
    <p>{{ msg }}</p>
  </div>
</template>


<script>
import axios from "axios";
export default {
  name: "BricksTest", //should be multi-word
  data() {
    return {
      msg: "Not FoundGG", 
    };
  },
  methods: {
    getResponse() {
      const path = "http://35.194.196.179:5000/";
      axios
        .get(path)
        .then((res) => {
          console.log(res.data);
          this.msg = res.data;
        })
        .catch((err) => {
          console.error(err);
        });
    },
  },
  created() {
    this.getResponse();
  },
};
</script>
