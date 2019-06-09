import Vue from "vue"

Vue.filter("dateDe", function(str) {
    if (str === null) {
        return ""
    }
    return str
        .split("-")
        .reverse()
        .join(".")
})

export function formatPriceEUR(n) {
    if (n === null || n == 0) {
        return "0,00€"
    }
    const c = 2
    const d = ","
    const t = "."
    var s = n < 0 ? "-" : "",
        i = String(parseInt((n = Math.abs(Number(n) || 0).toFixed(c)))),
        j = (j = i.length) > 3 ? j % 3 : 0

    return (
        s +
        (j ? i.substr(0, j) + t : "") +
        i.substr(j).replace(/(\d{3})(?=\d)/g, "$1" + t) +
        (c
            ? d +
              Math.abs(n - i)
                  .toFixed(c)
                  .slice(2)
            : "") +
        "€"
    )
}

Vue.filter("priceEUR", formatPriceEUR)
