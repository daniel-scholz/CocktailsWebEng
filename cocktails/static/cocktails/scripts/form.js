window.onload = function() {
  document.getElementById("id_picture").addEventListener("change", function(e) {
    input = e.target;
    if (input.files && input.files[0]) {
      var reader = new FileReader();
      reader.onload = function(e) {
        document.getElementById("pic").setAttribute("src", e.target.result);
      };
      reader.readAsDataURL(input.files[0]);
    }
  });
  ingredient_counter = 0;
  this.document.getElementById("add-ingredient-btn").onclick = newIngredient;
  function newIngredient() {
    let ingredient_list = document.getElementsByClassName("ingredient-list")[0];
    const ingredient_fields = [
      "remove",
      "ingredient_name",
      "amount",
      "unit",
      "is_alcohol"
    ];
    let new_ingredient = document.createElement("div");

    for (field of ingredient_fields) {
      const id = "id_" + field + "_" + ingredient_counter;
      if (field != "remove") {
        let label = document.createElement("label");
        label.setAttribute("for", id);
        label.appendChild(document.createTextNode(field));

        new_ingredient.appendChild(label);
      }

      const text_field = createInputField(id);
      new_ingredient.setAttribute("class", "ingredient");
      new_ingredient.setAttribute("style", "display:block; margin: 5px 0;");
      new_ingredient.setAttribute("id", "ingredient_" + ingredient_counter);
      new_ingredient.appendChild(text_field);
      ingredient_list.insertBefore(new_ingredient,ingredient_list.childNodes[0]);
    }

    let is_not_alcohol = document.createElement("input");
    is_not_alcohol.setAttribute("id", "id_hidden" + ingredient_counter);
    is_not_alcohol.setAttribute("name", "is_not_alcohol");
    is_not_alcohol.setAttribute("value", 1);
    is_not_alcohol.setAttribute("hidden", "");
    new_ingredient.appendChild(is_not_alcohol);
    document
      .getElementById("ingredient_counter")
      .setAttribute("value", ++ingredient_counter);

    function createInputField(id) {
      let text_field = document.createElement("input");
      text_field.setAttribute("id", id);
      text_field.setAttribute("name", field);
      text_field.setAttribute("required", "");
      if (field == "remove") {
        text_field.setAttribute("type", "button");
        text_field.setAttribute("value", "-");
        text_field.setAttribute("class", "remove-btn btn");
        text_field.addEventListener("click", function(event) {
          event.preventDefault();
          const id = event.target.id.split("_");
          document.getElementById("ingredient_" + id[id.length - 1]).remove();
          document
            .getElementById("ingredient_counter")
            .setAttribute("value", --ingredient_counter);
        });
      } else if (field === "amount") text_field.setAttribute("type", "number");
      else if (field === "is_alcohol") {
        text_field.removeAttribute("required");
        text_field.setAttribute("type", "checkbox");
        text_field.addEventListener("change", function(e) {
          e.preventDefault();
          let hidden_field = this.parentNode.childNodes[
            this.parentNode.childNodes.length - 1
          ];
          if (hidden_field.getAttribute("value") == 1)
            hidden_field.setAttribute("value", 0);
          else hidden_field.setAttribute("value", 1);
        });
      }
      return text_field;
    }
  }
};
