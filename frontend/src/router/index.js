import Vue from 'vue'
import Router from 'vue-router'
import sse from '@/components/sse'
import ws from '@/components/ws'

Vue.use(Router)

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/sse_poll',
      name: 'poll',
      component: sse
    },
    {
      path: '/ws_poll',
      name: 'poll',
      component: ws
    }
  ]
})
