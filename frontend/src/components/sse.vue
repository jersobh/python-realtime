<template>
  <div class="hello">
    <h2>Running over Server-sent Events</h2>
    <column-chart :data="[['Cruzeiro', datasource.cruzeiro], ['Atlético-MG', datasource.atletico]]" :colors="['#0d47a1', '#333']" :animation="false"></column-chart>
    <button class="botao" @click="add_vote_cruzeiro()"> Cruzeiro </button>&nbsp;&nbsp;<button class="botao" @click="add_vote_atletico()"> Atlético - MG </button>
  </div>
</template>

<script>
import Vue from 'vue'
import VueChartkick from 'vue-chartkick'
import Chart from 'chart.js'
import axios from 'axios'

Vue.use(VueChartkick, {adapter: Chart})

export default {
  name: 'poll',
  data () {
    return {
      evtSource: null,
      datasource: {
        'cruzeiro': 0,
        'atletico': 0
      },
      msg: 'Welcome to Your Vue.js App'
    }
  },
  methods: {
    add_vote_cruzeiro: function () {
    axios
      .post('https://localhost/vote_cruzeiro')
    },
    add_vote_atletico: function () {
    axios
      .post('https://localhost/vote_atletico')
    }
  },
  mounted () {
    let self = this
    self.evtSource = new EventSource("https://localhost/sse/");
    self.evtSource.onmessage = function(e) {
      let data = JSON.parse(e.data);
      self.datasource.cruzeiro = data.cruzeiro
      self.datasource.atletico = data.atletico
    }

  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1, h2 {
  font-weight: normal;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}


</style>
