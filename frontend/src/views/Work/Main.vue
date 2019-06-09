<template lang="pug">
div
    v-layout(v-if="hashbang === 'crew'", row, wrap, justify-center)
        v-flex(xs12)
            v-text-field(label="Leiter", disabled, :value="workHeadName")
            v-autocomplete(:items="headlessCrew", v-model="workCrew" multiple, chips, item-text="full_name", item-value="id", deletable-chips, @input="crewChanged = true")
        v-layout(v-if="crewChanged", justify-end)
            v-btn(color="secondary", flat, @click="discardCrewChanges") Verwerfen
            fancy-button(@click='saveCrewChanges', ref="saveCrewChanges") Speichern
    div(v-else) 
        timetable(:works="[work]",, style="margin: 0 -24px", @assign-crew="onAssignCrew")
</template>

<script>
import Timetable from "./../../components/Timetable.vue"
export default {
    name: "Work",
    components: {
        Timetable
    },
    data: function() {
        return {
            id: null,
            event: null,
            view: "",
            workCrew: [],
            crewChanged: false,
            assignCrewDialog: false
        }
    },
    computed: {
        hashbang() {
            return this.$route.hash.substr(1)
        },
        work() {
            return this.$store.getters.work
        },
        workHeadName() {
            if (this.crew && this.work) {
                let head = this.crew.find(x => x.id === this.work.head)
                return head ? head.full_name : ""
            }
            return ""
        },
        crew() {
            return this.$store.state.crew
        },
        headlessCrew() {
            if (this.crew && this.work) {
                return this.crew.filter(x => x.id !== this.work.head)
            }
            return []
        },
        workCrewInfo() {
            if (this.crew && this.work) {
                return this.crew.filter(x => this.work.crew.includes(x.id))
            }
            return []
        }
    },
    watch: {
        hashbang() {
            this.onHashbangChange()
        }
    },
    mounted() {
        this.id = this.$route.params.work
        this.event = this.$route.params.event
        this.$store.commit("setWork", this.id)
        this.fetch()
        if (this.hashbang !== "") {
            this.onHashbangChange()
        }
    },
    beforeDestroy() {
        this.$store.commit("title", "")
    },
    methods: {
        fetch() {
            this.$store
                .dispatch("fetchEvent", this.event)
                .then(() => {
                    this.$store.commit("title", this.$store.getters.work.name)
                    this.workCrew = this.$store.getters.work.crew
                    console.log(this.workCrew)
                })
                .catch(error => console.log(error))
        },
        onHashbangChange() {
            if (this.hashbang === "crew") {
                this.fetchCrew()
            } else if (this.hashbang === "shifts") {
                this.fetchCrew()
            }
        },
        fetchCrew() {
            this.$store.dispatch("fetchCrew")
        },
        discardCrewChanges() {
            this.workCrew = this.work.crew
            this.crewChanged = false
        },
        saveCrewChanges() {
            let payload = {
                crew: this.workCrew
            }
            this.$http
                .put(`/api/work/${this.work.id}`, payload)
                .then(response => {
                    this.$refs.saveCrewChanges.success().then(() => {
                        this.crewChanged = false
                    })
                    this.fetch()
                })
                .catch(error => {
                    this.$refs.saveCrewChanges.error()
                })
        },
        onAssignCrew(shift) {
            this.fetchCrew()
            this.$refs.crewChanges.open(shift)
        },
        assignCrewDialogSave() {
            this.$http
                .put(`/api/shift/${this.assignCrewDialogShift}`, {
                    crew: this.assignCrewDialogCrew
                })
                .then(response => {
                    this.$refs.assignCrewDialogSave.success()
                    this.assignCrewDialog = false
                })
                .catch(error => {
                    console.log(error)
                    this.$refs.assignCrewDialogSave.error()
                })
        }
    }
}
</script>
<style>
</style>
