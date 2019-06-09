<template lang="pug">
v-card(flat)
    v-card-title.display-1.login.primary.white--text Login
    v-card-text
        v-form(v-model='valid')
            v-text-field(v-model='username', type='text', label='Email', :rules='nameRules', :error="errors.length > 0", @input="onInput", required)
            v-text-field(v-model='password', type='password', label='Passwort', :rules='nameRules', :error-messages="errors", @input="onInput", required)
            br
            div.text-xs-center
                fancy-button(:disabled='!valid', @click='submit', ref="loginButton", submit) Einloggen

</template>



<script>
export default {
    name: "Login",

    data: () => ({
        valid: false,
        username: "",
        nameRules: [
            v => !!v || "Name is required"
            //v => v.length <= 10 || "Name must be less than 10 characters"
        ],
        password: "",
        errors: []
    }),
    mounted() {
        if (this.$store.getters.loggedIn) {
            this.$router.replace("/")
        }
    },
    methods: {
        onInput() {
            this.errors.splice(0, this.errors.length)
        },
        submit() {
            if (this.valid) {
                const data = {
                    email: this.username,
                    password: this.password
                }
                store
                    .dispatch("obtainToken", data)
                    .then(() => {
                        this.$refs.loginButton.success()
                        router.push("/")
                    })
                    .catch(status => {
                        this.$refs.loginButton.error()
                    })
            }
        }
    }
}
</script>

<style scoped>
.v-card {
    max-width: 300px;
    margin: auto;
}

.login {
    background: #212121;
    height: 72px;
    justify-content: center;
    user-select: none;
}
</style>
