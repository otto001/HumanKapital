<template lang="pug">
v-layout(justify-center)
    v-flex(xs12, sm8, md6)
        v-card(flat)
            v-card-title.display-1 Meine Daten
            v-card-text
                v-form(v-model='valid')
                    v-layout(row, wrap, justify-start)
                        v-flex(xs6)
                            v-text-field(v-model='fistName', type='text', :rules='nameRules', label='Vorname', required)
                        v-flex(xs6)
                            v-text-field(v-model='lastName', type='text', :rules='nameRules', label='Nachname', required)
                        
                        v-flex(xs12)
                            v-text-field(v-model='email', type='email', :rules='emailRules', label='Email', required)

                        v-flex(xs12)
                            v-text-field(v-model='phone', type='tel', label='Mobilnummer')

                        v-flex(xs3)
                            v-select(:items="shirtSizes", v-model="shirtSize", label="TShirt Größe")
                        v-flex(xs9)
                        v-flex(xs3)
                            v-switch(v-model="vat", color="primary", label="Vorsteuerabzugsberechtigt")
                        
                    br
                    div.text-xs-center
                        fancy-button(:disabled='!valid', @click='submit', ref="registerButton") Speichern

</template>



<script>
import { emailMatch } from "@/utils"

export default {
    name: "Register",

    data: () => ({
        valid: false,
        fistName: "",
        lastName: "",
        email: "",
        shirtSize: "",
        mobile: "",
        phone: "",
        vat: null,
        nameRules: [v => !!v || "Pflichfeld"],
        emailRules: [
            v => !!v || "Pflichfeld",
            v => !!emailMatch(v) || "Email ist nicht gültig"
        ],
        passwordRules: [
            v => !!v || "Pflichfeld",
            v => v.length >= 8 || "Password muss mindestens 8 Zeichen lang sein"
        ],

        shirtSizes: ["xs", "s", "m", "l", "xl", "xxl"]
    }),
    watch: {
        "$store.state.auth.user"() {
            this.update()
        }
    },
    mounted() {
        this.update()
    },
    methods: {
        update() {
            if (!this.$store.state.auth.user) return
            this.fistName = this.$store.state.auth.user.first_name
            this.lastName = this.$store.state.auth.user.last_name
            this.email = this.$store.state.auth.user.email
            this.shirtSize = this.$store.state.auth.user.shirt_size
            this.phone = this.$store.state.auth.user.phone
            this.vat = this.$store.state.auth.user.vat
        },
        submit() {
            if (this.valid) {
                const data = {
                    email: this.email,
                    first_name: this.fistName,
                    last_name: this.lastName,
                    shirt_size: this.shirtSize,
                    phone: this.phone,
                    vat: this.vat
                }
                this.$http
                    .put("/api/self", data)
                    .then(response => {
                        this.$refs.registerButton.success()
                    })
                    .catch(error => {
                        this.$refs.registerButton.error()
                    })
            }
        }
    }
}
</script>

<style scoped>
</style>
