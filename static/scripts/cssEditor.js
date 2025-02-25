// JS to scan the editor and make changes to the webpage as they're selected

// Getting the varibales that can be changed from the CSS
var editable = document.querySelector(':root');
// Getting the calues of saif varibales
var values = getComputedStyle(editable);

// Acquire the elements of the webpage that will be scanned for edits being made

/////////////////////////////////////////////////////////////////////////////////
// Color picker vars
var colorPicker = document.getElementById('color_banner');
var colorValue = document.getElementById('color-hex');
////////////////////////////////////////////////////////////////////////////////

////////////////////////////////////////////////////////////////////////////////
// Drop title text
var title = document.getElementById('title');
var titleValue = document.getElementById('drop-title');
var titleWeight = document.querySelectorAll('input[name="weight"]');
var fontColor = document.getElementById('color_font');
var borderThickness = document.getElementById('border');
var borderColor = document.getElementById('color_border');


console.log("cssEditor Loaded");

// Method to change color theme
colorPicker.addEventListener("input", function(){
    colorValue.innerText = colorPicker.value; // Displays the hex of the current selected color
    editable.style.setProperty('--background_color', colorPicker.value);
});

// Method to change the drop title text
title.addEventListener("input", function(){
    titleValue.innerText = title.value; // Display the new title on the banner
});

//Method to change the drop title font weights
titleWeight.forEach((weight) => {
    weight.addEventListener("click", function(){
        titleValue.style.fontWeight = weight.value;
        console.log(weight.value);
    });
});

// Method to change font color
fontColor.addEventListener("input", function(){
    editable.style.setProperty('--font_color_title', fontColor.value);
});

// Method to change border thickness
borderThickness.addEventListener("input", function(){
    editable.style.setProperty('--font_border_thickness', borderThickness.value);
    titleValue.style.paintOrder = 'stroke fill';
});

// Method to change the border color of the title
borderColor.addEventListener("input", function(){
    editable.style.setProperty('--font_border_color', borderColor.value);
});

