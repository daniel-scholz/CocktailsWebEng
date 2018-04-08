window.onload = function () {
    console.log("top5 loaded");
    let option = document.getElementsByClassName("option")
    for (o of option) {
        o.addEventListener("click", function (e) {
            e.preventDefault();
            let hiddenOption = document.getElementById("hidden-option")
            hiddenOption.setAttribute("value", this.innerText.toLowerCase())
            form = this.closest("form");
            if (form)
                findAncestor(this, ".option-form");
            form.submit()
        });
    }
};

function findAncestor(el, cls) {
    while ((el = el.parentElement) && !el.classList.contains(cls)) ;
    return el;
}
