<template lang="pug">
div
    event-dialog(v-model="eventDialogOpen")
    v-list(two-line subheader avatar)
        v-subheader(event) {{event ? "Event": "Events"}}
        transition-group(name="event-list")
            v-list-tile.event-list-tile(v-for="e in shownEvents", :key="e.id", router-link, :to="'/event/' + e.id", ripple)
                v-list-tile-avatar
                    v-icon event
                v-list-tile-content
                    v-list-tile-title {{e.name}}
                    v-list-tile-sub-title {{(new Date(e.start).toLocalISODate()) | dateDe}} - {{new Date(e.end).toLocalISODate() | dateDe}}
            template(v-if="event")
                v-list.event-details-list(avatar, dense, :key="'D-'+event.id")
                    v-list-tile(v-for="work in works", :key="work.id", router-link, :to="'/event/' + event.id + '/work/' + work.id", ripple)
                        v-list-tile-avatar
                            v-avatar(:color="work.color", :size="32")
                                v-icon(dark) {{work.icon}}
                        v-list-tile-content
                            v-list-tile-title {{work.name}}
                    v-list-tile(router-link, :to="'/event/' + event.id + '/total'")
                        v-list-tile-avatar
                            v-icon list
                        v-list-tile-content Gesamtübersicht

        v-list-tile(ripple, @click="eventDialogOpen = true",  v-if="$store.getters.hasPerm('add_event') && !event")
            v-list-tile-avatar
                v-icon add
            v-list-tile-content
                v-list-tile-title Neues Event
        
        //v-divider.mt-3
        //v-list-tile(ripple, router-link, to="/myshifts")
            v-list-tile-avatar
                v-icon TBD
            v-list-tile-content
                v-list-tile-title Meine Schichten
        
        template(v-if="$store.getters.hasPerm('crew_account_management')")
            v-divider.mt-3
            v-subheader Crew
            v-list-tile(ripple, router-link, to="/crew/activate")
                v-list-tile-avatar
                    v-icon person_add
                v-list-tile-content
                    v-badge.list-inline(color="primary", :value="crewNotActivated > 0")
                        span(slot="badge") {{crewNotActivated}}
                        v-list-tile-title Neue Registrierungen

            v-list-tile(ripple, router-link, to="/crew/create")
                v-list-tile-avatar
                    v-icon person_add
                v-list-tile-content
                    v-list-tile-title Neue Crew anlegen
</template>

<script>
import EventDialog from "./../components/dialogs/EventDialog.vue"
export default {
    name: "IndexNav",
    components: {
        EventDialog
    },
    data: function() {
        return {
            ready: false,
            crewNotActivated: 0,
            eventDialogOpen: false
        }
    },
    computed: {
        events() {
            return this.$store.state.events
        },
        crewAccountManagementPerm() {
            return this.$store.getters.hasPerm("crew_account_management")
        },
        event() {
            return this.$route.params.event ? this.$store.state.event : null
        },
        works() {
            if (!this.event) return {}
            return this.$store.state.works
        },
        shownEvents() {
            return this.event ? [this.event] : this.events
        }
    },
    watch: {
        crewAccountManagementPerm() {
            if (this.crewAccountManagementPerm) {
                this.getCrewNotActivated()
            }
        }
    },
    methods: {
        getCrewNotActivated() {
            this.$http
                .get("/api/crew/notactivated/count")
                .then(response => {
                    this.crewNotActivated = response.data
                })
                .catch(error => {
                    console.error(error)
                })
        }
    }
}
</script>

<style>
.list-inline .v-badge__badge {
    right: -30px;
    top: 0px;
    user-select: none;
}
.v-list__tile__title {
    width: fit-content;
    margin-right: 0;
}

.event-details-list .v-list__tile {
    padding-left: 40px;
}
.event-list-tile {
    transition: all 0s;
    transition: transform 0.3s;
}
.event-list-enter,
.event-list-leave-to {
    opacity: 0;
}
.event-list-leave-active {
    height: 0;
    opacity: 0;
}
</style>
