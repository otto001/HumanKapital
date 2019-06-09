<template lang="pug">
v-app
    global-events(@dragstart="closeDrawerOnMobile()")
    v-navigation-drawer(v-if="!noDrawer", v-model='drawer', app, style='margin-right: 0;', clipped, fixed)
        router-view(name='nav')
        index-nav(v-show="showDefaultNavbar")
    v-toolbar(app, clipped-left, fixed)
        v-toolbar-side-icon(v-if="!noDrawer", @click.stop='userToggleDrawer')
        v-toolbar-title.headline.text-uppercase

            
            logo(v-if="$vuetify.breakpoint.smAndUp || !routeTitle" @click='toIndex')
            v-layout(v-else-if="$vuetify.breakpoint.xsOnly", align-center, justify-start)
                v-flex(shrink)
                    div.opaque.route-title(@click='toIndex') {{routeTitle}}
                v-flex(shrink)
                    div.router-toolbar-mobile(v-if="$vuetify.breakpoint.xsOnly")
                        router-view(name='toolbar')
        v-spacer
        
        div.toolbar-title-center(v-if="$vuetify.breakpoint.smAndUp")
            div
                span.toolbar-title-center__title.headline.text-uppercase.route-title {{routeTitle}}

        
        router-view(name='toolbar')
        div(style="width: 16px;")
        user-avatar(v-if="userAvatar !== ''")
        v-btn(color='secondary', v-else-if="showRegister", router-link, to="/register") Registrieren
        v-btn(color='secondary', v-else-if="showLogin", router-link, to="/login") Login
    v-content
        v-container(fluid)
            router-view()

</template>

<script>
import GlobalEvents from "vue-global-events"
import UserAvatar from "@/components/UserAvatar.vue"
import Logo from "@/components/Logo.vue"
import Vue from "vue"
import IndexNav from "./views/IndexNav.vue"

export default {
    name: "App",
    components: {
        GlobalEvents,
        UserAvatar,
        IndexNav,
        Logo
    },
    data() {
        return {
            drawer: true,
            drawerBeforeRoute: false,
            lastDrawerWasUser: false,
            userMenu: false
        }
    },
    watch: {
        $route() {
            this.routeDrawer()
        }
    },
    computed: {
        userAvatar() {
            return store.state.auth.user !== null
                ? store.state.auth.user.first_name[0]
                : ""
        },
        userNameFull() {
            return store.state.auth.user !== null
                ? store.state.auth.user.first_name +
                      " " +
                      store.state.auth.user.last_name
                : ""
        },
        showRegister() {
            return (
                store.getters.loggedIn === false &&
                this.$route.name != "register"
            )
        },
        showLogin() {
            return (
                store.getters.loggedIn === false && this.$route.name != "login"
            )
        },
        routeTitle() {
            return this.$store.state.title || this.$route.meta.title || ""
        },
        showDefaultNavbar() {
            let matchedRoute = this.$route.matched[
                this.$route.matched.length - 1
            ]
            return matchedRoute ? !matchedRoute.components.nav : false
        },
        noDrawer() {
            if (!this.$route) return true
            return this.$route.meta.noDrawer || false
        }
    },
    created() {
        this.drawerBeforeRoute = this.drawer
        Vue.prototype.$closeDrawer = this.closeDrawer
        Vue.prototype.$closeDrawerOnMobile = this.closeDrawerOnMobile
        Vue.prototype.$openDrawer = this.openDrawer
        store
            .dispatch("refreshToken")
            .then(() => {})
            .catch(error => {
                router.push("/login")
            })
    },
    methods: {
        logout() {
            store.dispatch("deleteToken").then(() => {
                window.location.reload()
            })
        },
        toIndex() {
            router.push("/")
        },
        closeDrawerOnMobile() {
            if (this.$vuetify.breakpoint.mdAndDown) {
                this.drawer = false
            }
        },
        openDrawer() {
            this.drawer = true
            this.lastDrawerWasUser = false
        },
        closeDrawer() {
            this.drawer = false
            this.lastDrawerWasUser = false
        },
        userToggleDrawer() {
            this.drawer = !this.drawer
            this.drawerBeforeRoute = this.drawer
            this.lastDrawerWasUser = true
        },
        routeDrawer() {
            if (this.$vuetify.breakpoint.lgAndUp) {
                if (this.$route.meta.drawer === true) {
                    if (this.lastDrawerWasUser) {
                        this.drawerBeforeRoute = this.drawer
                        this.lastDrawerWasUser = false
                    }
                    this.drawer = true
                } else if (this.$route.meta.drawer === false) {
                    if (!this.lastDrawerWasUser) {
                        this.drawerBeforeRoute = this.drawer
                        this.lastDrawerWasUser = false
                    }
                    this.drawer = false
                } else if (!this.lastDrawerWasUser) {
                    this.drawer = this.drawerBeforeRoute
                }
            }
        }
    }
}
</script>
<style scoped>
.route-title {
    word-wrap: none;
    white-space: nowrap;
    text-overflow: ellipsis;
    overflow: hidden;
    max-width: 30vw;
}
.toolbar-title-center {
    position: absolute;
    width: 100%;
    text-align: center;
    pointer-events: none;
    user-select: none;
    left: 0;
}
.toolbar-title-center > div {
    text-align: center;
}
.toolbar-title-center__title {
    display: inline-block;
    padding: 10px;
}

.center-router-toolbar {
    width: 0;
    height: 0;
    position: relative;
    display: inline-block;
    vertical-align: top;
    z-index: 100;
    pointer-events: all;
}

.center-router-toolbar__content {
    display: inline-block;
    position: absolute;
}

.router-toolbar-mobile,
.router-toolbar-mobile * {
    opacity: 1;
}
</style>
