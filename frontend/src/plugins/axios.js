import axios from "axios"
import VueAxios from "vue-axios"
import Vue from "vue"
import consts from "@/consts"

let base = consts.baseUrl
if (base && base[0] != "/") base = "/" + base

axios.defaults.baseURL = base

Vue.use(VueAxios, axios)
