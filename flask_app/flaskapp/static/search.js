
function search_recipe() {
    let input = document.getElementById('searchbar').value;
    input = input.toLowerCase();
    let recipe = document.getElementsByClassName('recipe');
    
    for (i = 0; i < recipe.length; i++) { 
        if (!recipe[i].getElementsByTagName('a')[0].innerHTML.toLowerCase().includes(input)) {
            recipe[i].style.display="none";
        }
        else {
            recipe[i].classList.remove("dissappear");
            recipe[i].style.display="list-item";                 
        }
        document.getElementsByClassName("pagination")[0].style.display = "none";
    }
    if(input == "") {
        filter_recipes(true);
        document.getElementsByClassName("pagination")[0].style.display = "";
    }


}
