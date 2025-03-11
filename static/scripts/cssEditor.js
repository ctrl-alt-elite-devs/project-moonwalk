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
////////////////////////////////////////////////////////////////////////////////

////////////////////////////////////////////////////////////////////////////////
// Image Banner
var compositionChoices = document.querySelectorAll('input[name="composition"]');
var image00 = document.getElementById("image00");
var image01 = document.getElementById("image01");
var image02 = document.getElementById("image02");
var maxwidth00 = 430; // Layout 1 (default)
var maxheight00 = 331; // Layout 1 (default)
var maxwidth01 = 430; // Layout 1 (default)
var maxheight01 = 331; // Layout 1 (default)
var maxwidth02 = 430; // Layout 1 (default)
var maxheight02 = 331; // Layout 1 (default)
var inputImg00 = document.getElementById("img00");
var inputImg01 = document.getElementById("img01");
var inputImg02 = document.getElementById("img02");
////////////////////////////////////////////////////////////////////////////////

////////////////////////////////////////////////////////////////////////////////
// Submit button
var submit = document.getElementById("done");
////////////////////////////////////////////////////////////////////////////////

console.log("cssEditor Loaded");

// Method to change color theme
colorPicker.addEventListener("input", function(){
    colorValue.innerText = colorPicker.value; // Displays the hex of the current selected color
    editable.style.setProperty('--background_color', colorPicker.value);
});

// Method to change the composition of the images
// May have to scrap image compositions
compositionChoices.forEach((composition) => {
    composition.addEventListener("click", function(){
        if (composition.value == 'composition00'){
            maxheight00 = 331
            maxheight01 = 331; 
            maxheight02 = 331;
            maxwidth00 = 430;
            maxwidth01 = 430; 
            maxwidth02 = 430;
        }
        if (composition.value == 'composition01'){
            maxwidth00 = 645;
            maxwidth01 = 645;
            maxwidth02 = 645;
            maxheight00 = 331;
            maxheight01 = 165;
            maxheight02 = 165;
            console.log(maxwidth00);
        }
        if (composition.value == 'composition02'){
            
        }
    });
});

// Method to change displayed images
inputImg00.onchange = function(){
    image00.style.width = maxwidth00+'px';
    image00.style.height = maxheight00+'px';
    image00.style.backgroundSize = 100;
    image00.src = URL.createObjectURL(inputImg00.files[0]);
}
inputImg01.onchange = function(){
    image01.style.width = maxwidth01+'px';
    image01.style.height = maxheight01+'px';
    image01.src = URL.createObjectURL(inputImg01.files[0]);
}
inputImg02.onchange = function(){
    image02.style.width = maxwidth02+'px';
    image02.style.height = maxheight02+'px';
    image02.src = URL.createObjectURL(inputImg02.files[0]);
}

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

// Method to submit changes to server
submit.addEventListener("click", function(){
    console.log("submitted");
});

