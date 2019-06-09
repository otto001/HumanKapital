import axios from "axios"

export default {
    state: {
        user: null,
        djangoUserId: null,
        permissions: [],
        is_superuser: false,
        endpoints: {
            obtainJWT: "/auth/token/obtain",
            refreshJWT: "/auth/token/refresh",
            deleteJWT: "/auth/token/delete"
        }
    },
    getters: {
        loggedIn: state => {
            return state.djangoUserId !== null
        },
        hasPerm: state => codename => {
            return state.is_superuser || state.permissions.includes(codename)
        }
    },
    mutations: {
        setDjangoUser(state, data) {
            if (!data) {
                state.djangoUserId = null
                state.groups = []
                return
            }
            console.log(data)
            state.djangoUserId = data["user"]
            state.permissions = data["permissions"]
            state.is_superuser = data["is_superuser"]
        },
        resetUser(state) {
            state.user = null
        },
        setUserData(state, data) {
            state.user = data
        },
        setGroups(state, data) {
            state.groups = data
        }
    },
    actions: {
        updateUser({ state, commit }) {
            if (state.djangoUserId === 0) return
            axios
                .get("/api/self")
                .then(response => {
                    this.commit("setUserData", response.data)
                })
                .catch(error => {
                    console.error(error)
                })
            this.dispatch("init")
        },
        obtainToken({ state, commit }, params) {
            const payload = {
                email: params.email,
                password: params.password
            }
            return new Promise((resolve, reject) => {
                axios
                    .post(state.endpoints.obtainJWT, payload)
                    .then(response => {
                        if ("user" in response.data) {
                            commit("setDjangoUser", response.data)
                            this.dispatch("updateUser")
                        } else {
                            console.warn("no user provided")
                        }
                        resolve()
                    })
                    .catch(error => {
                        try {
                            reject(error.response["status"])
                        } catch {
                            reject(null)
                        }
                    })
            })
        },

        refreshToken({ state, commit }) {
            return new Promise((resolve, reject) => {
                axios
                    .post(state.endpoints.refreshJWT)
                    .then(response => {
                        if ("user" in response.data) {
                            commit("setDjangoUser", response.data)
                            this.dispatch("updateUser")
                        } else {
                            console.warn("no user provided")
                        }
                        resolve()
                    })
                    .catch(error => {
                        try {
                            reject(error.response["status"])
                        } catch {
                            reject(null)
                        }
                    })
            })
        },
        deleteToken({ state, commit }) {
            return new Promise((resolve, reject) => {
                axios
                    .post(state.endpoints.deleteJWT)
                    .then(() => {
                        this.commit("resetUser")
                        commit("setDjangoUser", null)
                        resolve()
                    })
                    .catch(error => {
                        try {
                            reject(error.response["status"])
                        } catch {
                            reject(null)
                        }
                    })
            })
        }
    }
}
