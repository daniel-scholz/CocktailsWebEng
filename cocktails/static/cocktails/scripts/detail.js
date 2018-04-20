window.onload = function () {
    var voteButtons = document.getElementsByClassName("vote-buttons")[0];
    console.log(voteButtons.childNodes);
    for (vb of voteButtons.childNodes) {
        if (vb instanceof Element && !vb.closest("form").classList.contains("inactive")) {
            vb.addEventListener("click", function (e) {
                e.preventDefault();
                let vote = document.getElementById("vote");
                if (this.classList.contains("arrow-up")) {
                    vote.setAttribute("value", "up");
                    console.log("click-up")

                }
                else if (this.classList.contains("arrow-down")) {
                    console.log("click-down");
                    vote.setAttribute("value", "down")
                }
                e.target.closest(".vote-form").submit()
            })
        }
    }

    var checkboxes = document.getElementsByClassName("check-field");
    for (c of checkboxes) {
        if (c instanceof Element) {
            c.addEventListener("change", function (e) {
                //console.log(this.parentNode.childNodes)

                for (b of this.parentNode.childNodes) {
                    if (b instanceof Element && b.getAttribute("name") === "on_shopping_list") {
                        if (b.value === b.id + ":True") {
                            b.setAttribute("value", b.id + ":False")
                        } else {
                            b.setAttribute("value", b.id + ":True")
                        }
                        console.log(b)
                    }
                }
            })
        }
    }
};
