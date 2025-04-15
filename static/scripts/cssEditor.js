
// JS to scan the editor and make changes to the webpage as they're selected

// Getting the varibales that can be changed from the CSS
var editable = document.querySelector(':root');
// Getting the calues of saif varibales
var values = getComputedStyle(editable);

// Acquire the elements of the webpage that will be scanned for edits being made

// Getting the drop date data
var dropDate = document.getElementById('date-drop');

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
var fontStyle = document.querySelectorAll('input[name="font_style"]');
var fontColor = document.getElementById('color_font');
var borderThickness = document.getElementById('border');
var borderColor = document.getElementById('color_border');
////////////////////////////////////////////////////////////////////////////////

////////////////////////////////////////////////////////////////////////////////
// Image Banner
var compositionChoices = document.querySelectorAll('input[name="composition"]');
var image00 = document.getElementById("image00");
var image01 = document.getElementById("image01");
var image02 = document.getElementById("image02");
var maxwidth = 518;
var maxheight = 331;
var inputImg00 = document.getElementById("img00");
var inputImg01 = document.getElementById("img01");
var inputImg02 = document.getElementById("img02");
////////////////////////////////////////////////////////////////////////////////

////////////////////////////////////////////////////////////////////////////////
// Submit and Cancel button
var submit = document.getElementById("done");
var cancel = document.getElementById("cancel");
////////////////////////////////////////////////////////////////////////////////


// Method to change color theme
colorPicker.addEventListener("input", function(){
    colorValue.innerText = colorPicker.value; // Displays the hex of the current selected color
    editable.style.setProperty('--background_color', colorPicker.value);
});

// Method to change displayed images
inputImg00.onchange = function(){
    image00.style.width = maxwidth+'px';
    image00.style.height = maxheight+'px';
    image00.style.backgroundSize = 100;
    image00.src = URL.createObjectURL(inputImg00.files[0]);
    image00.style.objectFit = "cover";
}
inputImg01.onchange = function(){
    image01.style.width = maxwidth+'px';
    image01.style.height = maxheight+'px';
    image01.src = URL.createObjectURL(inputImg01.files[0]);
    image01.style.objectFit = "cover";
}
inputImg02.onchange = function(){
    image02.style.width = maxwidth+'px';
    image02.style.height = maxheight+'px';
    image02.src = URL.createObjectURL(inputImg02.files[0]);
    image02.style.objectFit = "cover";
}

//Method to chnage the font style
fontStyle.forEach((font_style) => {
    font_style.addEventListener("click", function(){
        titleValue.style.fontFamily = font_style.value;
        console.log(font_style.value);
    });
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


// Method used when cancel is pressed (Revert)
cancel.addEventListener("click", function(){
    console.log("cancel");
});