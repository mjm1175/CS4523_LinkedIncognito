var settingsMenu = document.querySelector(".settings-menu");
var darkBtn = document.getElementById("dark-btn");

function settingsMenuToggle() {
    settingsMenu.classList.toggle("settings-menu-height");

}

var deleteMenu = document.querySelector(".delete-menu");

function deleteMenuToggle() {
    deleteMenu.classList.toggle("delete-menu-height");
}


darkBtn.onclick = function(){
    darkBtn.classList.toggle("dark-btn-on");
    document.body.classList.toggle("dark-theme")

    if (localStorage.getItem("theme") == "light") {
        localStorage.setItem("theme", "dark");
    }

    else {
        localStorage.setItem("theme", "light");
    }
}

if(localStorage.getItem("theme") == "light") {
    darkBtn.classList.remove("dark-btn-on");
    document.body.classList.remove("dark-theme");
}

else if (localStorage.getItem("theme") == "dark") {
    darkBtn.classList.add("dark-btn-on");
    document.body.classList.add("dark-theme");
}

else {
    localStorage.setItem("theme", "light");
    localStorage.getItem("theme");
}


// function that hides/shows field_four based upon field_three value
function check_field_value(new_val) {
    if(new_val == 'No') {
        // #id_field_four should be actually the id of the HTML element
        // that surrounds everything you want to hide.  Since you did
        // not post your HTML I can't finish this part for you.  
        $('#upload-resume-direct').hide();
    } else {
        $('#upload-resume-direct').show();
    }
}


// function that hides/shows field_four based upon field_three value
function check_field_value2() {
    if($(this).val() == 'No') {
        // #id_field_four should be actually the id of the HTML element
        // that surrounds everything you want to hide.  Since you did
        // not post your HTML I can't finish this part for you.  
        $('#upload-cover-direct').hide();
    } else {
        $('#upload-cover-direct').show();
    }
}


// this is executed once when the page loads
$(document).ready(function() {
    // set things up so my function will be called when field_three changes
    $('#prof-resume').change(function() {
        check_field_value(this.value)
    });
    $('#prof-cover').change(check_field_value2);

    // set the state based on the initial values
    //check_field_value.call($('#prof-resume').get(0));
    check_field_value2.call($('#prof-cover').get(0));

});


// function that hides/shows field_four based upon field_three value
function check_field_value(new_val) {
    console.log('in func');    
    if(new_val != ' Yes') {
        // #id_field_four should be actually the id of the HTML element
        // that surrounds everything you want to hide.  Since you did
        // not post your HTML I can't finish this part for you.  
        console.log('not yes');        
        $('#upload-resume-direct').hide();
    } else {
        console.log('yes yes');        
        $('#upload-resume-direct').show();
    }
}


