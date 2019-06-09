<template lang="pug">
div()
    new-work-dialog(v-model="newWorkDialogOpen", @created="getEvent")
    event-dialog(v-model="eventDialogOpen", :from-store="true")
    v-layout(row wrap justify-center align-center)
        v-btn(
            v-for="work in works"
            :key="work.id"
            router-link
            :to="'/event/' + id + '/work/' + work.id"
            align-center
            class="square") 
            v-icon(v-if="work.icon", :color="work.color") {{work.icon}}
            span {{work.name}}

    v-layout.mt-3(row wrap justify-center align-center)
    
        v-btn.square(
            router-link
            :to="'/event/' + id + '/total'"
            align-center) 
            v-icon list
            span Gesamtübersicht

        v-btn(
            v-if="$store.getters.hasPerm('add_work')"
            @click="newWorkDialogOpen = true"
            align-center
            class="square") 
            v-icon add
            span Neues Gewerk

        v-btn.square(
            router-link
            :to="'/event/' + id + '/roles'"
            align-center) 
            v-icon category
            span Rollen
        
        v-btn.square(
            router-link
            :to="'/event/' + id + '/stats'"
            align-center) 
            v-icon timeline
            span Statistik

        v-btn.square(align-center, @click="eventDialogOpen = true") 
            v-icon edit
            span Eventdaten ändern
</template>

<script>
import NewWorkDialog from "@/components/dialogs/NewWorkDialog.vue"
import EventDialog from "@/components/dialogs/EventDialog.vue"

export default {
    name: "Event",
    components: {
        NewWorkDialog,
        EventDialog
    },
    data: function() {
        return {
            id: null,
            newWorkDialogOpen: false,
            eventDialogOpen: false
        }
    },
    computed: {
        works() {
            return this.$store.state.works
        }
    },
    watch: {
        $route: {
            handler() {
                this.id = this.$route.params.event
                this.getEvent()
            },
            immediate: true
        }
    },
    methods: {
        getEvent() {
            this.$store.dispatch("fetchEvent", this.id)
        }
    }
}
</script>

<style>
.square {
    width: 200px;
    max-width: unset;
    height: 200px;
    border-radius: 8px;
}
.square div {
    position: absolute;
    top: 0;
    bottom: 0;
}
.square .v-icon {
    font-size: 600%;
}
.square span {
    bottom: 10px;
    position: absolute;
}
</style>
