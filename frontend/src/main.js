import Vue from "vue"
import "./plugins/vuetify"
import "./plugins/axios"
import router from "./router"
import store from "./store"
import "./filters"
import "./utils"

import App from "./App.vue"
import VueDragDrop from "vue-drag-drop"
import Chartkick from "vue-chartkick"
import Chart from "chart.js"
import "@mdi/font/css/materialdesignicons.css"
import FancyButton from "@/components/ui/FancyButton.vue"
import Stateful from "@/components/Stateful.vue"
import "@/assets/style.styl"

Vue.config.productionTip = false

Vue.component("fancy-button", FancyButton)
Vue.component("stateful", Stateful)

Vue.use(VueDragDrop)
Vue.use(Chartkick.use(Chart))

var app = new Vue({
    router,
    store,
    render: h => h(App)
})
global.app = app

window.store = store
global.store = store

window.router = router
global.router = router

app.$mount("#app")
store.dispatch("fetchEvents").catch(error => {
    console.log(error)
})
