import axios from "axios"
import Vuex from "vuex"
import auth from "./jwt"
import filters from "./filters"
import Vue from "vue"

Vue.use(Vuex)

export default new Vuex.Store({
    modules: {
        auth,
        filters
    },
    state: {
        event: null,
        works: null,
        workId: null,
        events: null,
        crew: [],
        title: "",
        timetableZoom: 1.0
    },
    getters: {
        work(state) {
            if (state.works) {
                return state.works[state.workId]
            }
            return null
        }
    },
    mutations: {
        title(state, title) {
            state.title = title
        },
        setEvents(state, events) {
            state.events = events
        },
        setCrew(state, crew) {
            state.crew = crew.map(x => {
                return { ...x, full_name: x.first_name + " " + x.last_name }
            })
        },
        setEvent(state, event) {
            state.event = event
            if (state.event && state.event.roles) {
                state.event.roles = state.event.roles.reduce((map, obj) => {
                    map[obj.id] = obj
                    return map
                }, {})
            }
        },
        setWorks(state, works) {
            state.works = works
            if (!works) return
            state.works = state.works.map(x => {
                x.tasks = x.tasks.reduce((map, obj) => {
                    map[obj.id] = obj
                    return map
                }, {})
                return x
            })
            state.works = state.works.reduce((map, obj) => {
                map[obj.id] = obj
                return map
            }, {})
        },
        setWork(state, id) {
            state.workId = id
        },
        timetableZoom(state, zoom) {
            state.timetableZoom = zoom
        }
    },
    actions: {
        init() {
            this.dispatch("fetchEvents").catch(error => {
                console.log(error)
            })
        },
        fetchEvents({ state, commit }) {
            return new Promise((resolve, reject) => {
                axios
                    .get("/api/events")
                    .then(response => {
                        commit("setEvents", response.data)
                        resolve()
                    })
                    .catch(error => {
                        reject()
                    })
            })
        },
        fetchCrew({ state, commit }) {
            return new Promise((resolve, reject) => {
                axios
                    .get("/api/crew/list")
                    .then(response => {
                        commit("setCrew", response.data)
                        resolve()
                    })
                    .catch(error => {
                        reject()
                    })
            })
        },
        fetchEvent({ state, commit }, id = null) {
            return new Promise((resolve, reject) => {
                if (id) {
                    if (state.event !== null && state.event.id === id) resolve()
                } else if (state.event) {
                    id = state.event.id
                    if (!id) reject()
                } else {
                    reject()
                }

                axios
                    .get("/api/event/" + id)
                    .then(response => {
                        commit("setEvent", response.data)
                    })
                    .catch(error => {
                        reject()
                    })
                axios
                    .get("/api/works?event=" + id)
                    .then(response => {
                        commit("setWorks", response.data)
                        resolve()
                    })
                    .catch(error => {
                        reject()
                    })
            })
        }
    }
})
