<template lang="pug">
v-layout(justify-center)
    v-flex(xs12, md6)
        v-card(flat)
            v-card-title
                span.headline.mb-0 Neue Crew Mitglieder
            v-card-text
                v-list(two-line)
                    v-list-tile(v-for="crew in crewNotActivated", :key="crew.id")
                        v-list-tile-content
                            v-list-tile-title {{crew.first_name}} {{crew.last_name}}
                            v-list-tile-sub-title {{new Date(crew.time_registered).toLocalISODate() | dateDe}} {{new Date(crew.time_registered).toLocalISOTime()}}
                        v-list-tile-action.crew-actions

                            //v-flex
                            //    v-btn(color="error", icon, flat) 
                            //        v-icon clear
                            v-btn(color="success", icon, flat, @click="acceptCrewMember(crew.id)") 
                                v-icon done
</template>

<script>
export default {
    name: "CrewActivate",
    data() {
        return {
            crewNotActivated: []
        }
    },
    mounted() {
        this.getCrewNotActivated()
    },
    methods: {
        getCrewNotActivated() {
            this.$http
                .get("/api/crew/notactivated")
                .then(response => {
                    this.crewNotActivated = response.data
                    if (this.$getNav(0)) {
                        this.$getNav(
                            0
                        ).crewNotActivated = this.crewNotActivated.length
                    }
                })
                .catch(error => {
                    console.error(error)
                })
        },
        acceptCrewMember(pk) {
            this.$http
                .post("/api/crew/" + pk + "/activate")
                .then(response => {
                    console.log(response)
                    this.getCrewNotActivated()
                })
                .catch(error => {
                    console.error(error)
                })
        }
    }
}
</script>

<style scoped>
.crew-actions {
    width: 77px;
    flex-direction: row;
    justify-content: end;
    display: grid;
}
</style>
