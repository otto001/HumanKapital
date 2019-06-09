<template lang="pug">
div
    timetable(:works="works", style="margin: 0 -24px")

</template>

<script>
import NewWorkDialog from "@/components/dialogs/NewWorkDialog.vue"
import Timetable from "@/components/Timetable.vue"

export default {
    name: "EventTotal",
    components: {
        NewWorkDialog,
        Timetable
    },
    data: function() {
        return {
            id: null,
            works: [],
            newWorkDialogOpen: false
        }
    },
    mounted() {
        this.id = this.$route.params.event
        this.getEvent()
        this.getWorks()
    },
    methods: {
        getEvent() {
            this.$store.dispatch("fetchEvent", this.id)
        },
        getWorks() {
            this.$http
                .get("/api/works?event=" + this.id)
                .then(response => {
                    this.works = response.data
                    for (let work of this.works) {
                        work.tasks = work.tasks.reduce((map, obj) => {
                            map[obj.id] = obj
                            return map
                        }, {})
                    }
                })
                .catch(error => {
                    console.error(error)
                })
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
