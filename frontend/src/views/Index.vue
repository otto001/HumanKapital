<template lang="pug">
v-layout
    v-flex
        v-sheet(height='500')
            v-calendar(:now='today', :value='today', color='primary')
                template(slot='day', slot-scope='{ date }')
                    template(v-for='event in eventsMap[date]')
                        div.event-tile.body-2(:style="getEventSytle(event, date)", @click="linkToEvent(event.id)") {{event.name}}
                            

</template>

<script>
export default {
    name: "Events",

    data: function() {
        return {
            today: new Date().toLocalISODate()
        }
    },
    computed: {
        events() {
            return this.$store.state.events
        },
        eventsMap() {
            const map = {}
            if (this.events) {
                this.events.forEach(e => {
                    let d = new Date(e.start)
                    while (d < new Date(e.end)) {
                        ;(map[d.toLocalISODate()] =
                            map[d.toLocalISODate()] || []).push(e)
                        d.setHours(d.getHours() + 24)
                    }
                })
            }

            return map
        }
    },
    methods: {
        linkToEvent(e) {
            this.$router.push(`/event/${e}`)
        },
        getEventSytle(event, date) {
            let style = { "background-color": this.$vuetify.theme.primary }
            let widthExtra = 0

            date = new Date(date)
            date.setHours(date.getHours() + 24)
            let nextDateString = new Date(date).toLocalISODate()
            date.setHours(date.getHours() - 2 * 24)
            let prevDateString = new Date(date).toLocalISODate()
            if (
                this.eventsMap[nextDateString] &&
                this.eventsMap[nextDateString].find(x => (x.id = event.id))
            ) {
                widthExtra += 5
                style["border-top-right-radius"] = 0
                style["border-bottom-right-radius"] = 0
            }
            if (
                this.eventsMap[prevDateString] &&
                this.eventsMap[prevDateString].find(x => (x.id = event.id))
            ) {
                widthExtra += 4
                style["margin-left"] = "-4px"
                style["border-top-left-radius"] = 0
                style["border-bottom-left-radius"] = 0
            }
            if (widthExtra) {
                style["width"] = `calc(100% + ${widthExtra}px)`
            }
            return style
        }
    }
}
</script>

<style>
.event-tile {
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    border-radius: 2px;
    color: #ffffff;
    width: 100%;
    padding: 3px;
    cursor: pointer;
    margin-bottom: 1px;
}

.v-calendar-weekly__day {
    overflow: visible;
}
</style>
