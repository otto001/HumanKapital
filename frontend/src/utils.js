/** Function that count occurrences of a substring in a string;
 * @param {String} string               The string
 * @param {String} subString            The sub string to search for
 * @param {Boolean} [allowOverlapping]  Optional. (Default:false)
 *
 * @author Vitim.us https://gist.github.com/victornpb/7736865
 * @see Unit Test https://jsfiddle.net/Victornpb/5axuh96u/
 * @see http://stackoverflow.com/questions/4009756/how-to-count-string-occurrence-in-string/7924240#7924240
 */
export function occurrences(string, subString, allowOverlapping = false) {
    string += ""
    subString += ""
    if (subString.length <= 0) return string.length + 1

    var n = 0,
        pos = 0,
        step = allowOverlapping ? 1 : subString.length

    while (true) {
        pos = string.indexOf(subString, pos)
        if (pos >= 0) {
            ++n
            pos += step
        } else break
    }
    return n
}

export function removeA(arr) {
    var what,
        a = arguments,
        L = a.length,
        ax
    while (L > 1 && arr.length) {
        what = a[--L]
        while ((ax = arr.indexOf(what)) !== -1) {
            arr.splice(ax, 1)
        }
    }
    return arr
}

Date.prototype.toLocalISODate = function() {
    return new Date(this.getTime() - this.getTimezoneOffset() * 60 * 1000)
        .toISOString()
        .substring(0, 10)
}

Date.prototype.toLocalISOTime = function() {
    return new Date(this.getTime() - this.getTimezoneOffset() * 60 * 1000)
        .toISOString()
        .substring(11, 16)
}

Date.prototype.toISOTime = function() {
    return this.toISOString().substring(11, 16)
}

Date.prototype.toISODate = function() {
    return this.toISOString().substring(0, 10)
}

Date.prototype.getWeek = function() {
    // Copy date so don't modify original
    let d = new Date(
        Date.UTC(this.getFullYear(), this.getMonth(), this.getDate())
    )
    // Set to nearest Thursday: current date + 4 - current day number
    // Make Sunday's day number 7
    d.setUTCDate(d.getUTCDate() + 4 - (d.getUTCDay() || 7))
    // Get first day of year
    var yearStart = new Date(Date.UTC(d.getUTCFullYear(), 0, 1))
    // Calculate full weeks to nearest Thursday
    var weekNo = Math.ceil(((d - yearStart) / 86400000 + 1) / 7)
    // Return array of year and week number
    return weekNo
}

export function pad(num, size) {
    var s = num + ""
    while (s.length < size) s = "0" + s
    return s
}

export function emailMatch(email) {
    return email.match(
        /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
    )
}

export function centsToMoney(cents) {
    cents = cents.toString()
    return (
        cents.substr(0, cents.length - 2) +
        "." +
        cents.substr(cents.length - 2, 2)
    )
}

export function moneyToCents(money) {
    return parseInt(money.replace(/\./, ""))
}
