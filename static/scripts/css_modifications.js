
// Get access to all editable variables
var editable = document.querySelector(':root');

// Extract the information stored in ':root'
var editable_s = getComputedStyle(editable);


function modifyAppearance(){
    alert ("You will be prompted to edit the CSS now.");
    console.log("Current background color is " + editable_s.getPropertyValue('--background_color'));
    console.log("What do you want the new color to be?");

    let background_color = prompt("New background color: ");

    if (background_color !== null){
        editable.style.setProperty('--background_color', background_color);
    }
}

modifyAppearance();