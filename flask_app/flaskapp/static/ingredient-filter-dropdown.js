const filters = [];

function filter_recipes(isAuthenticated) {
    let recipes = document.getElementsByClassName('recipe');
    
    if(filters.length > 0) {
        for (i = 0; i < recipes.length; i++) { 
            let found = true;
            let currList = recipes[i].getElementsByTagName('ul')[0].getElementsByTagName('li');

            //Comparison algorithm
            for(const ingr of currList) {
                let bool = false
                for(const filter of filters) {
                    if(ingr.innerHTML.toLowerCase().includes(filter)) {
                        bool = true;
                        break;
                    }
                }
                if(!bool) {
                    found = false;
                    break;
                }
            }

            if(found && !isAuthenticated) {
                if(!recipes[i].classList.contains("showing")) {
                    recipes[i].classList.remove("dissappear");
                    recipes[i].classList.add("appear");
                    recipes[i].classList.remove("hiding");
                    recipes[i].classList.add("showing");
                }
            }
            else if(found && isAuthenticated) {
                if(!recipes[i].classList.contains("showing")) {
                    recipes[i].classList.remove("hiding");
                    recipes[i].classList.add("showing");
                }
            }
            else {
                if(!recipes[i].classList.contains("hiding")) {
                    recipes[i].classList.remove("appear");
                    recipes[i].classList.add("dissappear"); 
                    recipes[i].classList.remove("showing");
                    recipes[i].classList.add("hiding");
                }
            }
        }
    }
    else {
        for (i = 0; i < recipes.length; i++) {
            recipes[i].classList.remove("dissappear");
            recipes[i].classList.add("appear");
            recipes[i].classList.remove("hiding");
            recipes[i].classList.add("showing");
            // recipes[i].style.display = "list-item";
        }
    }

    paginate(1);
}

function adjust_filters() {
    filters.length = 0;
    let curr_filters = document.getElementsByClassName("form-check-input");
    for (i = 0; i < curr_filters.length; i++) {
        if(curr_filters[i].checked == true) {
            filters.push(curr_filters[i].value.toLowerCase());
        }
    }
    show_missing_ingr();
    filter_recipes(false);
}

function show_all() {
    let recipes = document.getElementsByClassName('recipe');
    
    //displays hidden recipes as well as their missing ingredients
    for (i = 0; i < recipes.length; i++) {
        if(recipes[i].style.display != "list-item") {
            recipes[i].classList.remove("dissappear");
            recipes[i].classList.add("appear");
            recipes[i].classList.remove("hiding");
            recipes[i].classList.add("showing");
            // recipes[i].style.display = "list-item";
        }
    }

    show_missing_ingr();
    paginate(1);
}

function show_missing_ingr() {
    let recipes = document.getElementsByClassName('recipe');

    //displays hidden recipes as well as their missing ingredients
    for (i = 0; i < recipes.length; i++) {
        const missing_ingr = []
        let currList = recipes[i].getElementsByTagName('ul')[0].getElementsByTagName('li');

        //Comparison algorithm
        for(const ingr of currList) {
            let found = false;
            for(const filter of filters) {
                if(ingr.innerHTML.toLowerCase().includes(filter)) {
                    found = true;
                    break;
                }
            }

            if(!found) {
                missing_ingr.push(ingr.innerHTML)
            }
        }

        const div = document.createElement('div');
        div.setAttribute('class', 'col m-3');
        div.setAttribute('id', 'placeholder-' + (i+1));
        //Creates a missing elements list in the html
        
        const h6 = document.createElement('h6');
        h6.textContent = 'Missing Ingredients:'
        const ul = document.createElement('ul');
        for (const ingr of missing_ingr) {
            const li = document.createElement('li');
            li.textContent = ingr;
            ul.appendChild(li);
        }
        if(missing_ingr.length == 0) {
            const li = document.createElement('li');
            li.setAttribute('style', 'color: #c4c2c2')
            li.textContent = "None!";
            ul.appendChild(li);
        }
        div.setAttribute('style', 'color: #636161;');
        div.appendChild(h6);
        div.appendChild(ul); 
        
        const placeholder = document.getElementById("placeholder-" + (i+1));
        placeholder.parentNode.replaceChild(div, placeholder);
    }
}
 