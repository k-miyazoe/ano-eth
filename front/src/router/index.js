import Vue from 'vue'
import VueRouter from 'vue-router'
import HomeView from '../views/HomeView.vue'
import SignUp from '../views/SignUp.vue'
import SignIn from '../views/SignIn.vue'
import Question from '../components/Question.vue'
import QuestionView from '../components/QuestionView.vue'


Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/about',
    name: 'about',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
  },
  {
    path: '/signup',
    component: SignUp
  },
  {
    path: '/signin',
    component: SignIn
  },
  {
    path: '/question',
    component: Question
  },
  //動的に質問閲覧ページを表示する必要がある
  {
    path: '/question/:id',
    component: QuestionView
  },


]

const router = new VueRouter({
  routes
})

export default router
