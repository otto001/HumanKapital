<template lang="pug">
v-layout(justify-center)
    v-flex(xs12, sm8, md6)
        v-card(flat)
            v-card-title.display-1 Benutzer anlegen
            v-card-text
                v-form(v-model='valid')
                    v-layout(row, wrap)
                        v-flex(xs6)
                            v-text-field(v-model='firstName', type='text', :rules='nameRules', label='Vorname', required)
                        v-flex(xs6)
                            v-text-field(v-model='lastName', type='text', :rules='nameRules', label='Nachname', required)
                        
                        v-flex(xs12)
                            v-text-field(v-model='email', type='text', :rules='emailRules', label='Email', required)
                        v-flex(xs12)
                            v-text-field(v-model='password', type='password', :rules='passwordRules', label='Passwort', required)
                        v-flex(xs3)
                            v-switch(v-model="superuser", color="primary", label="Admin")
                        
                    br
                    div.text-xs-center
                        fancy-button(:disabled='!valid', @click='submit', ref="registerButton", persitent-success, submit) Erstellen

</template>



<script>
import { emailMatch } from "@/utils"

export default {
    name: "UserCreate",

    data: () => ({
        valid: false,
        firstName: "",
        lastName: "",
        email: "",
        password: "",
        superuser: false,
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
                    first_name: this.firstName,
                    last_name: this.lastName,
                    superuser: this.superuser
                }
                this.$http
                    .post("/api/crew/create", data)
                    .then(response => {
                        this.$refs.registerButton.success().then(() => {
                            this.email = ""
                            this.firstName = ""
                            this.lastName = ""
                            this.password = ""
                            this.superuser = false
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
