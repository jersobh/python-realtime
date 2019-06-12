<template>
  <div class="hello">
    <h2>Running over Server-sent Events</h2>
    <column-chart :data="[['Cruzeiro', datasource.cruzeiro], ['Atlético-MG', datasource.atletico]]" :colors="['#0d47a1', '#333333', '#0d47a1', '#333333']" :animation="false"></column-chart>
    <div class="row" style="max-width:100%;"> 
     <b>{{datasource.cruzeiro}}</b>
    <img src="cruzeiro.png" @click="add_vote_cruzeiro()" style="max-width:40%;max-height:120px;cursor:pointer;padding:1%;"></img>
    <img src="atleticomg.png" @click="add_vote_atletico()" style="max-width:40%;max-height:120px;cursor:pointer;padding:1%;"></img>
    <b>{{datasource.atletico}}</b>
    </div>
  </div>
</template>

<script>
import Vue from 'vue/dist/vue.js';
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
      .post('/vote_cruzeiro')
    },
    add_vote_atletico: function () {
    axios
      .post('/vote_atletico')
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
