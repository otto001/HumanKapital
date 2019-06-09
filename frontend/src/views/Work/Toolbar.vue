<template lang="pug">
    div
        v-layout
            v-select.page-sel(width="120", label="", :items="items", item-text="name", item-value="val", v-model="selected", solo, flat, @input="onSwitch")
            work-filters
            
</template>

<script>
import WorkFilters from "@/components/WorkFilters.vue"

export default {
    name: "WorkToolbar",
    components: { WorkFilters },
    data: function() {
        return {
            selected: "shifts",
            items: [
                { val: "shifts", name: "Schichten" },
                { val: "crew", name: "Crew" }
            ]
        }
    },
    mounted() {
        if (this.$route.hash === "") {
            this.$router.replace("#" + this.selected)
        } else {
            this.selected = this.$route.hash.substr(1)
        }
    },
    methods: {
        onSwitch(newVal) {
            this.selected = newVal
            this.$router.push("#" + this.selected)
        }
    }
}
</script>

<style scoped>
.page-sel {
    max-width: 110px;
}
</style>
