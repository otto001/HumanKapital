<template lang="pug">
div
    v-layout(justify-end, align-center)
        v-btn(flat, round, @click="toToday") Heute
        v-select.caltype-sel(dense, solo, flat, :items="calTypes", item-text="[1]", item-value="[0]", v-model="calType")

        v-btn(icon, @click="pageFlip(-1)")
            v-icon chevron_left
        v-btn(icon, @click="pageFlip(1)")
            v-icon chevron_right

</template>

<script>
export default {
    name: "MyShiftsOverviewToolbar",
    components: {},
    data: function() {
        return {
            calDate: new Date("2019-05-01").toISODate(),
            calTypes: [
                ["month", "Monat"],
                ["week", "Woche"],
                ["4day", "4 Tage"],
                ["day", "Tag"]
            ],
            calType: "month"
        }
    },
    computed: {},
    watch: {
        calType() {
            this.$router.push({
                query: { ...this.$route.query, type: this.calType }
            })
        },
        calDate() {
            this.$router.push({
                query: { ...this.$route.query, date: this.calDate }
            })
        },
        $route() {
            if (
                this.$route.query.type &&
                this.$route.query.type != this.calType
            ) {
                this.calType = this.$route.query.type
            }
            if (
                this.$route.query.date &&
                this.$route.query.date != this.calDate
            ) {
                this.calDate = this.$route.query.date
            }
        }
    },
    mounted() {
        this.calType = this.$route.query.type || this.calTypes[0][0]
    },
    methods: {
        pageFlip(direction) {
            let calDate = new Date(this.calDate)
            var offset = 0
            switch (this.calType) {
                case "month":
                    calDate.setMonth(calDate.getMonth() + direction)
                    break

                case "week":
                    offset = 7
                    break

                case "4day":
                    offset = 4
                    break
                case "day":
                    offset = 1
                    break
            }
            calDate = calDate.getTime() + direction * offset * 86400000
            this.calDate = new Date(calDate).toISODate()
        },
        toToday() {
            this.calDate = new Date().toISODate()
        }
    }
}
</script>

<style lang="stylus">
.caltype-sel {
  max-width: 110px;
}

.caltype-sel .v-input__slot {
  margin-bottom: 0;
  height: 32px;
}
</style>
