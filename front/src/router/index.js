import Vue from 'vue'
import VueRouter from 'vue-router'
import HomeView from '../views/HomeView.vue'
import SignUp from '../views/SignUp.vue'
import SignIn from '../views/SignIn.vue'
import MyPage from '../views/MyPage.vue'
import Question from '../components/Question.vue'
import QuestionView from '../components/QuestionView.vue'
import CreateEther from '../views/CreateEther.vue'
//import MyPage from '../views/Mypage.vue'
import NotFoundComponent from '../components/NotFoundComponent.vue'


Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
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
    path: '/create-question',
    component: Question
  },
  //動的に質問閲覧ページを表示する必要がある
  {
    path: '/question/:id',
    component: QuestionView,
    props: true,
    name: "question-detail"
  },
  {
    path: '/create-ether',
    component: CreateEther,
  },
  {
    path: '/mypage',
    component: MyPage,
    props: true,
    name: "mypage"
  },
  {
    path: '*',
    component: NotFoundComponent,
    name: 'notFound',
  }

]

const router = new VueRouter({
  mode: 'history',
  routes
})

export default router
