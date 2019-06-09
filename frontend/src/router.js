import Vue from "vue"
import Router from "vue-router"
import consts from "@/consts"
import IndexView from "./views/Index.vue"
import IndexNav from "./views/IndexNav.vue"
import EventView from "./views/Event/Event.vue"
import EventRolesView from "./views/Event/EventRoles.vue"
import EventStatsView from "./views/Event/EventStats.vue"

import EventTotalView from "./views/Event/EventTotalView.vue"
import EventTotalToolbar from "./views/Event/EventTotalToolbar.vue"
import WorkView from "./views/Work/Main.vue"
import WorkNav from "./views/Work/Nav.vue"
import WorkToolbar from "./views/Work/Toolbar.vue"

import MyShiftsOverviewToolbar from "./views/MyShifts/MyShiftsOverviewToolbar.vue"
import MyShiftsOverview from "./views/MyShifts/MyShiftsOverview.vue"

Vue.use(Router)

Vue.prototype.$getDefault = function(index) {
    if (this.$route.matched.length) {
        index =
            typeof index === "number" ? index : this.$route.matched.length - 1
        return this.$route.matched[index].instances.default
    }
    return null
}

Vue.prototype.$getNav = function(index) {
    if (this.$route.matched.length) {
        index =
            typeof index === "number" ? index : this.$route.matched.length - 1
        return this.$route.matched[index].instances.nav
    }
    return null
}
console.log(consts.baseUrl)
export default new Router({
    mode: "history",
    base: consts.baseUrl,
    routes: [
        {
            path: "/",
            components: {
                default: IndexView
                //nav: IndexNav
            },
            meta: {
                drawer: true
            }
        },
        {
            path: "/event/:event",
            components: {
                default: EventView
            }
        },
        {
            path: "/event/:event/total",
            name: "event-total",
            components: {
                default: EventTotalView,
                toolbar: EventTotalToolbar
            },
            meta: {
                title: "Gesamtübersicht"
            }
        },
        {
            path: "/event/:event/roles",
            components: {
                default: EventRolesView
            },
            meta: {
                title: "Rollen"
            }
        },
        {
            path: "/event/:event/stats",
            components: {
                default: EventStatsView
            },
            meta: {
                title: "Statistik"
            }
        },
        {
            path: "/event/:event/work/:work",
            components: {
                default: WorkView,
                toolbar: WorkToolbar
            },
            meta: {
                title: "Gewerk",
                drawer: true
            }
        },

        {
            path: "/crew",
            name: "crew",
            components: {
                default: () => import("./views/Crew/CrewBase.vue")
            },
            children: [
                {
                    path: "activate",
                    components: {
                        default: () => import("./views/Crew/CrewActivate.vue")
                    }
                },
                {
                    path: "create",
                    name: "create",
                    component: () => import("./views/Account/UserCreate.vue")
                }
            ]
        },
        {
            path: "/login",
            name: "login",
            component: () => import("./views/Account/Login.vue"),
            meta: {
                title: "",
                noDrawer: true
            }
        },
        {
            path: "/register",
            name: "register",
            component: () => import("./views/Account/Register.vue"),
            meta: {
                title: "Registrieren",
                noDrawer: true
            }
        },
        {
            path: "/account",
            name: "account",
            component: () => import("./views/Account/View.vue"),
            meta: {
                title: "Account"
            }
        },
        {
            path: "/myshifts",
            name: "myshifts",
            components: {
                default: MyShiftsOverview,
                toolbar: MyShiftsOverviewToolbar
            },
            meta: {
                drawer: false
            }
        }
    ]
})
