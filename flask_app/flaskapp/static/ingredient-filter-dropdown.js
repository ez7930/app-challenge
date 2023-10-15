const filters = [];

function filter_recipes() {
    let recipes = document.getElementsByClassName('recipe');
    if(filters.length > 0) {
        for (i = 0; i < recipes.length; i++) { 
            let currList = recipes[i].getElementsByTagName('ul')[0].getElementsByTagName('li');

            //matches filter to each ingredient in a recipe
            for(h = 0; h < currList.length; h++) {
                if(filters.indexOf(currList[h].innerHTML.toLowerCase()) < 0) {
                    //if it does not contain a filter it hides the recipe then moves onto the next one
                    recipes[i].style.display = "none"; 
                    break;
                }
                else {
                    recipes[i].style.display = "list-item";   
                }
            }
        }
    }
    else {
        for (i = 0; i < recipes.length; i++) {
            recipes[i].style.display = "list-item";
        }
    }
}

function adjust_filter(filter) {
    if(document.getElementById(filter).checked == true) {
        filters.push(filter);
        filter_recipes();
    }  
    else {
        const index = filters.indexOf(filter);
        if (index > -1) { // only splice array when item is found
            filters.splice(index, 1); // 2nd parameter means remove one item only
        }
        filter_recipes();
    }
}

function reset_checkboxes() {
    let checkboxes = document.getElementsByClassName("form-check-input");
    for(i = 0; i < checkboxes.length; i++) {
        checkboxes[i].checked = false;
    }
    filters.length = 0;
    filter_recipes();
}