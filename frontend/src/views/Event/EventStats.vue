<template lang="pug">
v-layout(wrap)
    v-flex(xs12)
        v-card
            v-card-title.headline Übersicht
            v-card-text
                v-layout
                    v-flex(xs12, md6).pr-3
                        table(v-if="overview", style="width: 100%")
                            tr
                                td Gesamtdauer
                                td.text-xs-right {{eventDurationFormatted}}
                            tr
                                td Gesamtkosten
                                td.text-xs-right {{costTotal | priceEUR}}
                            tr
                                td Gesamtarbeitszeit
                                td.text-xs-right {{worktimeTotal}}h
                    v-flex(xs12, md6).pl-3
                        table(v-if="overview", style="width: 100%")
                            tr
                                td Schichten
                                td.text-xs-right {{overview.shift_count}}
                            tr
                                td Crew Headcount
                                td.text-xs-right {{overview.assigned_crew}}
                            tr
                                td Geplante Einteilungen
                                td.text-xs-right {{overview.planned_staff_assignments}}
    v-flex(xs12, md6)
        v-card
            v-card-title.headline Kosten pro Gewerk
            v-card-text
                aggregation-visualisation(unit="EUR", :headers="['Gewerk', 'Kosten']", :breakdown="costPerWorkChart", :total="costTotal", :colors="costPerWorkColors")         
    v-flex(xs12, md6)
        v-card
            v-card-title.headline Kosten pro Rolle
            v-card-text
                aggregation-visualisation(unit="EUR", :headers="['Rolle', 'Kosten']", :breakdown="costPerRoleChart", :total="costTotal", :colors="null")         
    
    v-flex(xs12, md6, lg6)
        v-card
            v-card-title.headline Arbeitszeiten pro Gewerk
            v-card-text
                aggregation-visualisation(unit="h", :headers="['Gewerk', 'Arbeitszeit']", :breakdown="worktimePerWorkChart", :total="worktimeTotal", :colors="worktimePerWorkColors")         
    v-flex(xs12, md6, lg6)
        v-card
            v-card-title.headline Arbeitszeiten pro Rolle
            v-card-text
                aggregation-visualisation(unit="h", :headers="['Rolle', 'Arbeitszeit']", :breakdown="worktimePerRoleChart", :total="worktimeTotal", :colors="null")         

</template>

<script>
import { formatPriceEUR } from "@/filters"
import { pad } from "@/utils"

import AggregationVisualisation from "@/components/AggregationVisualisation.vue"

export default {
    name: "EventStats",
    components: { AggregationVisualisation },
    data: function() {
        return {
            id: null,
            cost: {},
            worktime: {},
            overview: {},
            costPerWorkChartType: 0,
            headers: [
                { text: "Gewerk", value: "name", sortable: true },
                {
                    text: "Kosten",
                    value: "cost",
                    align: "right",
                    sortable: true
                }
            ]
        }
    },
    computed: {
        works() {
            return this.$store.state.works
        },
        costTotal() {
            return this.cost.total
        },
        worktimeTotal() {
            return this.worktime.total
        },
        costPerWork() {
            return this.cost.per_work ? Object.entries(this.cost.per_work) : []
        },
        costPerWorkChart() {
            return this.costPerWork.map(([work, val]) => [
                this.$store.state.works[work].name,
                val
            ])
        },
        costPerWorkColors() {
            return this.costPerWork.map(
                ([work, val]) => this.$store.state.works[work].color
            )
        },
        costPerRole() {
            return this.cost.per_role ? Object.entries(this.cost.per_role) : []
        },
        costPerRoleChart() {
            return this.costPerRole.map(([role, val]) => [
                this.$store.state.event.roles[role].name,
                val
            ])
        },

        worktimePerWork() {
            return this.worktime.per_work
                ? Object.entries(this.worktime.per_work)
                : []
        },
        worktimePerWorkChart() {
            return this.worktimePerWork.map(([work, val]) => [
                this.$store.state.works[work].name,
                val
            ])
        },
        worktimePerWorkColors() {
            return this.worktimePerWork.map(
                ([work, val]) => this.$store.state.works[work].color
            )
        },
        worktimePerRole() {
            return this.worktime.per_role
                ? Object.entries(this.worktime.per_role)
                : []
        },
        worktimePerRoleChart() {
            return this.worktimePerRole.map(([role, val]) => [
                this.$store.state.event.roles[role].name,
                val
            ])
        },
        eventDurationFormatted() {
            if (!this.overview) return ""
            let seconds = this.overview.duration
            let days = Math.floor(seconds / 3600 / 24)
            let hours = Math.floor(seconds / 3600 - days * 24)

            let minutes = Math.floor(seconds / 60 - (days * 24 + hours) * 60)
            let result = `${pad(days, 2)}d`
            if (hours) {
                result += ` ${pad(hours, 2)}h`
                if (minutes) {
                    result += ` ${pad(minutes, 2)}min`
                }
            }
            return result
        }
    },
    watch: {
        $route: {
            handler() {
                this.id = this.$route.params.event
                this.getEvent()
                this.fetchOverview()
            },
            immediate: true
        }
    },
    methods: {
        getEvent() {
            this.$store.dispatch("fetchEvent", this.id)
        },
        fetchOverview() {
            this.$http
                .get(`/api/event/${this.id}/stats/overview`)
                .then(response => {
                    this.cost = response.data.cost
                    this.overview = response.data.overview
                    this.worktime = response.data.worktime
                })
                .catch(error => {
                    console.log(error)
                })
        }
    }
}
</script>
