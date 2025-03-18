
// Get the time from python using django
var remainingTime_str = data;
var remainingTime = parseFloat(remainingTime_str);
// console.log(remainingTime);
    

// Define the function that will update the html values
function updateCountdown(){
    console.log("Entered the function");
    // Get each time units values
    var days = Math.floor(remainingTime / 86400);
    var hours = Math.floor((remainingTime % 86400) / 3600);
    var minutes = Math.floor((remainingTime % 3600) / 60);
    var seconds = Math.floor(remainingTime % 60);

    //console.log(days)
    // console.log(hours)
        
    // Format each unit
    days_str = String.format("%02d", days);
    hours_str = String.format("%02d", hours);
    //minutes_str = String.format("%02d", minutes);
    //seconds_str = String.format("%02d", seconds);
    console.log(hours);


    // Update the values here

    // Check values for proper formatting "00"
    if (days < 10){
        document.getElementById("number_Days").innerHTML = "0" + days;
    } else {
        document.getElementById("number_Days").innerHTML = days;
    }

    if (hours < 10){
        document.getElementById("number_Hours").innerHTML = hours_str;
    } else {
        document.getElementById("number_Hours").innerHTML = hours_str;
    }

    if (minutes < 10){
        document.getElementById("number_Minutes").innerHTML = "0" + minutes;
    } else {
        document.getElementById("number_Minutes").innerHTML = minutes;
    }

    if (seconds < 10){
        document.getElementById("number_Seconds").innerHTML = "0" + seconds;
    } else {
        document.getElementById("number_Seconds").innerHTML = seconds;
    }
    

    // Check to see if no time remains
    if (remainingTime <= 0) {
        // Set values to 00
        clearInterval(update);
        document.getElementById("number_Days").innerHTML = "00";
        document.getElementById("number_Hours").innerHTML = "00";
        document.getElementById("number_Minutes").innerHTML = "00";
        document.getElementById("number_Seconds").innerHTML = "00";

    } else {
        remainingTime--;
    }
}
    
// Update the timer every second
var update = setInterval(updateCountdown, 1000);
