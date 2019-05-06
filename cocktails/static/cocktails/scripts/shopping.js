window.onload = function() {
  var rButtons = document.getElementsByClassName("remove-btn");
  for (butt of rButtons) {
    if (butt instanceof Element) {
      butt.addEventListener("click", function(e) {
        for (b of this.parentNode.childNodes) {
          if (b instanceof Element && b.classList.contains("check-field")) {
            console.log(b);
            if (b.value === b.id + ":True") {
              b.setAttribute("value", b.id + ":False");
            } else {
              b.setAttribute("value", b.id + ":True");
            }
            console.log(b);
          }
        }
      });
    }
  }
};
