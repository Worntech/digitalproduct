! function() {
    function e() { document.querySelector(".preloader").style.opacity = "0", document.querySelector(".preloader").style.display = "none" }
    window.onload = function() { window.setTimeout(e, 500) }, window.onscroll = function() { var e = document.querySelector(".navbar-area"),
            t = e.offsetTop;
        window.pageYOffset > t ? e.classList.add("sticky") : e.classList.remove("sticky"); var o = document.querySelector(".scroll-top");
        document.body.scrollTop > 50 || document.documentElement.scrollTop > 50 ? o.style.display = "flex" : o.style.display = "none" }, (new WOW).init(), document.querySelectorAll(".page-scroll").forEach((e => { e.addEventListener("click", (t => { t.preventDefault(), document.querySelector(e.getAttribute("href")).scrollIntoView({ behavior: "smooth", offsetTop: -59 }) })) })); let t = document.querySelector(".mobile-menu-btn");
    t.addEventListener("click", (function() { t.classList.toggle("active") })), new counterUp({ start: 0, duration: 2e3, intvalues: !0, interval: 100, append: " " }).start() }();