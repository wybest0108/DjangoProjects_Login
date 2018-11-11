$(function () {
    var currUrl = window.location.href,
        list = $(".nav.nav-sidebar li");
    for(var i = 0, len = list.length; i < len; ++i) {
        list[i].className = (currUrl.indexOf(list[i].id) == -1) ? "" : "active";
    }
});