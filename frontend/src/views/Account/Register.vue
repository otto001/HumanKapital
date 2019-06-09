<template lang="pug">
v-layout(justify-center)
    v-flex(xs12, sm8, md6)
        v-card(flat)
            v-card-title.display-1 Registrieren
            v-card-text
                v-form(v-model='valid')
                    v-layout(row, wrap)
                        v-flex(xs6)
                            v-text-field(v-model='fistName', type='text', :rules='nameRules', label='Vorname', required)
                        v-flex(xs6)
                            v-text-field(v-model='lastName', type='text', :rules='nameRules', label='Nachname', required)
                        
                        v-flex(xs12)
                            v-text-field(v-model='email', type='text', :rules='emailRules', label='Email', required)
                        v-flex(xs12)
                            v-text-field(v-model='password', type='password', :rules='passwordRules', label='Passwort', required)
                    br
                    div.text-xs-center
                        fancy-button(:disabled='!valid', @click='submit', ref="registerButton", persitent-success, submit) Registrieren

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
        password: "",
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
    methods: {
        submit() {
            if (this.valid) {
                const data = {
                    password: this.password,
                    email: this.email,
                    first_name: this.fistName,
                    last_name: this.lastName
                }
                this.$http
                    .post("/api/register", data)
                    .then(response => {
                        this.$refs.registerButton.success().then(() => {
                            this.$router.push("/login")
                        })
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
