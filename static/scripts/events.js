console.log("Fetching Google Calendar Events...");

document.addEventListener("DOMContentLoaded", function () {
    const eventSection = document.getElementById("events");

    if (!eventSection) {
        console.error("Error: Element with id='events' not found!");
        return;
    }

    const calendarId = "900fdf650b579a007feb6e7f8ac879190337d00eac8e62aeffbbb6cd9ff10df3@group.calendar.google.com";
    const apiKey = "AIzaSyD6F5dmxpASXeAYbaRIHZvymFVu4AluzWA";

    async function fetchEvents() {
        try {
            console.log("Fetching events...");
            const response = await fetch(
                `https://www.googleapis.com/calendar/v3/calendars/${calendarId}/events?key=${apiKey}&timeMin=${new Date().toISOString()}&orderBy=startTime&singleEvents=true`
            );

            if (!response.ok) {
                throw new Error(`HTTP Error! Status: ${response.status}`);
            }

            const data = await response.json();
            console.log("Fetched Events:", data); // Debugging log
            displayEvents(data.items);
        } catch (error) {
            console.error("Error fetching events:", error);
            eventSection.innerHTML = `<p> Error loading events: ${error.message}</p>`;
        }
    }

    function displayEvents(events) {
        eventSection.innerHTML = ""; // Clear previous content
    
        if (!events || events.length === 0) {
            eventSection.innerHTML = "<p>No upcoming events.</p>";
            return;
        }
    
        events.slice(0, 4).forEach(event => {
            let eventDate;
            let eventTime;
            let endTime = ""; // Default to empty in case there's no end time
    
            if (event.start.dateTime) {
                // If it's a timed event, use start and end time
                eventDate = new Date(event.start.dateTime);
                const endDate = event.end.dateTime ? new Date(event.end.dateTime) : null;
    
                eventTime = eventDate.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    
                if (endDate) {
                    endTime = ` - ${endDate.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}`;
                }
            } else {
                // If it's an all-day event, fix the timezone shift issue
                eventDate = new Date(event.start.date + "T00:00:00");
                eventDate.setMinutes(eventDate.getMinutes() + eventDate.getTimezoneOffset());
                eventTime = "All Day";
            }
    
            const eventElement = document.createElement("div");
            eventElement.classList.add("event-box");
    
            eventElement.innerHTML = `
                <p class="event-description">
                    <strong>Name:</strong> ${event.summary}<br>
                    <strong>Date:</strong> ${eventDate.toDateString()}<br>
                    <strong>Time:</strong> ${eventTime}${endTime}<br>
                    <a class="google-calendar-link" href="${event.htmlLink}" target="_blank">View on Google Calendar</a>
                </p>
            `;
    
            eventSection.appendChild(eventElement);
        });
    }
    

    // Fetch events when the page loads
    fetchEvents();
});
