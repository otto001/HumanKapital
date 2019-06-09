<template lang="pug">
div
    v-list
        v-list-tile(v-for="role in roles", :key="role.id", @click="$refs.dialog.open(role)")
            v-layout(justify-space-between)
                v-flex {{role.name}} 
                    span.short ({{role.short}})
                v-flex.rate {{role.rate | priceEUR}}/h
    role-dialog(ref="dialog")
        v-btn(slot="activator", color="primary", absolute, right) Neue Rolle


</template>

<script>
import RoleDialog from "@/components/dialogs/RoleDialog.vue"

export default {
    name: "EventRoles",
    components: { RoleDialog },
    data: function() {
        return {
            id: null
        }
    },
    mounted() {
        this.id = this.$route.params.event
        this.getEvent()
    },
    computed: {
        roles() {
            return this.$store.state.event ? this.$store.state.event.roles : []
        }
    },
    methods: {
        getEvent() {
            this.$store.dispatch("fetchEvent", this.id)
        }
    }
}
</script>

<style scoped>
.short {
    opacity: 0.54;
}

.rate {
    text-align: right;
}
</style>
