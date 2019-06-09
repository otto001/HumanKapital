import Vue from "vue"
import Vuetify from "vuetify/lib"
import "vuetify/src/stylus/app.styl"
import de from "vuetify/lib/locale/de"
import en from "vuetify/lib/locale/en"

Vue.use(Vuetify, {
    iconfont: "md",
    lang: {
        locales: { en, de },
        current: "de"
    },
    theme: {
        primary: "#98BF0F",
        secondary: "#424242",
        accent: "#82B1FF",
        error: "#FF5252",
        info: "#2196F3",
        success: "#4CAF50",
        warning: "#FFC107"
    }
})
