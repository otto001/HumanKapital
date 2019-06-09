<template lang="pug">
div
   
    v-layout
        v-flex
            v-sheet(height="84vh")
                v-calendar(:now='today', :value='calDate', color='primary', :type="calType", @click:date="dateClicked", @change="updateTitle", :weekdays="[1,2,3,4,5,6,0]")
                    template(#day="{ date }")
                        template(v-for='shift in shiftsMapDay[date]')
                            div.day-month.body-2.primary {{getShiftTitle(shift)}}
                    
                    template(v-slot:dayBody="{ date, timeToY, minutesToPixels }")
                        template(v-for='shift in shiftsMapDay[date]')
                            div.day-timed.body-2.primary(:style="getShiftTimedStyle(shift, timeToY, minutesToPixels)") {{getShiftTitle(shift)}}
                                div.sub-title {{getShiftSubTitle(shift)}}
            

</template>

<script>
export default {
    name: "MyShiftsOverview",
    components: {},
    data: function() {
        return {
            shifts: [],
            works: {},
            events: {},
            today: new Date().toISODate(),
            calTypes: ["month", "week", "4day", "day"]
        }
    },
    computed: {
        shiftsMapDay() {
            const map = {}
            if (this.shifts) {
                this.shifts.forEach(shift => {
                    let start = new Date(shift.start)
                    ;(map[start.toLocalISODate()] =
                        map[start.toLocalISODate()] || []).push(shift)
                })
            }

            return map
        },
        calType() {
            let calType = this.$route.query.type
            if (this.calTypes.includes(calType)) {
                return calType
            }
            return this.calTypes[0]
        },
        calDate() {
            return this.$route.query.date || this.today
        }
    },
    mounted() {
        this.fetch()
        if (this.calType === "month") {
            this.updateTitle({
                start: { date: this.calDate },
                end: { date: null }
            })
        }
    },
    beforeDestroy() {
        this.$store.commit("title", null)
    },
    methods: {
        fetch() {
            this.$http
                .get("/api/myshifts")
                .then(response => {
                    this.shifts = response.data.shifts
                    this.works = response.data.works.reduce((map, obj) => {
                        obj.tasks = obj.tasks.reduce((map, t) => {
                            map[t.id] = t
                            return map
                        }, {})
                        map[obj.id] = obj
                        return map
                    }, {})
                    this.events = response.data.events.reduce((map, obj) => {
                        map[obj.id] = obj
                        return map
                    }, {})
                })
                .catch(error => {
                    console.error(error)
                })
        },
        getShiftTitle(shift) {
            let work = this.works[shift.work]
            let task_name = work.tasks[shift.task].name
            return `${task_name}`
        },
        getShiftSubTitle(shift) {
            let work = this.works[shift.work]
            let task_name = work.tasks[shift.task].name
            let start = new Date(shift.start).toLocalISOTime()
            let end = new Date(shift.end).toLocalISOTime()
            return `${start} - ${end}`
        },
        getShiftTimedStyle(shift, timeToY, minutesToPixels) {
            let start = new Date(shift.start)
            let diff = new Date(shift.end) - start
            let duration = Math.round((diff % 86400000) / 60000)
            let startMinutes = start.getMinutes() + start.getHours() * 60
            return {
                top: timeToY(startMinutes) + "px",
                height: minutesToPixels(duration) + "px"
            }
        },

        dateClicked({ date }) {
            this.$router.push({
                query: { ...this.$route.query, date: date, type: "day" }
            })
        },
        updateTitle({ start, end }) {
            start = new Date(start.date)
            end = new Date(end.date)
            var title
            if (this.calType === "month") {
                title = start.toLocaleString("de-de", {
                    month: "long",
                    year: "numeric"
                })
            } else if (this.calType === "week") {
                title = "KW " + start.getWeek()
            } else if (this.calType === "4day") {
                title =
                    start.toLocaleString("de-de", {
                        day: "numeric",
                        month: "numeric"
                    }) +
                    " - " +
                    end.toLocaleString("de-de", {
                        day: "numeric",
                        month: "numeric",
                        year: "numeric"
                    })
            } else if (this.calType === "day") {
                title = start.toLocaleString("de-de", {
                    day: "numeric",
                    month: "long",
                    year: "numeric"
                })
            }

            this.$store.commit("title", title)
        }
    }
}
</script>

<style>
.day-month {
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    border-radius: 2px;
    width: 100%;
    padding: 3px;
    cursor: pointer;
    margin-bottom: 1px;
    color: white;
}

.day-timed {
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    border-radius: 2px;
    background-color: #1867c0;
    color: #ffffff;
    border: 1px solid #1867c0;
    font-size: 12px;
    padding: 3px;
    cursor: pointer;
    margin-bottom: 1px;
    left: 4px;

    position: absolute;
    right: 4px;
    margin-right: 0px;
}
</style>
<style scoped>
.caltype-sel {
    max-width: 100px;
}
</style>
