<template lang="pug">
    v-layout(justify-start style="margin-top: 10px" wrap)

        //new-shift-dialog(v-if="$store.state.event")

        v-btn(color="primary" round depressed v-if="false") 
            v-icon(left dark) add  
            | Neue Rolle 


        //
        v-flex(xs12)
            v-list(subheader)
                v-subheader() Aufgaben
                drag(v-for="(task, index) in tasks", :key="task.id", 
                     :transfer-data="{'type': 'new-shift', 'task': task.id}", drop-effect="move", effect-allowed="move")
                    v-list-tile(@click="")
                        v-list-tile-avatar
                            v-icon assignment
                        v-list-tile-content 
                            v-list-tile-title {{task.name}}
                new-task-dialog(style="width: 100%")
                    v-list-tile(slot="activator", @click="", ripple)
                        v-list-tile-avatar
                            v-icon add 
                        v-list-tile-content 
                            v-list-tile-title Neue Aufgabe
        
</template>

<script>
import NewTaskDialog from "@/components/dialogs/NewTaskDialog.vue"

export default {
    name: "WorkNav",

    components: {
        NewTaskDialog
    },

    data: function() {
        return {}
    },
    computed: {
        icon() {
            if (this.$store.getters.work) {
                return this.$store.getters.work.icon
            }
            return ""
        },
        tasks() {
            if (this.$store.getters.work) {
                return Object.values(this.$store.getters.work.tasks)
            }
            return []
        }
    },
    mounted() {},
    methods: {
        createTask() {}
    }
}
</script>
