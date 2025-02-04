console.log("JavaScript file loaded successfully!");

const calendarId = "900fdf650b579a007feb6e7f8ac879190337d00eac8e62aeffbbb6cd9ff10df3@group.calendar.google.com";
const apiKey = "AIzaSyD6F5dmxpASXeAYbaRIHZvymFVu4AluzWA";
const eventSection = document.getElementById("events");

// Get the current time in ISO format to show only future events
const now = new Date().toISOString();

async function fetchEvents() {
    try {
        const response = await fetch(
            `https://www.googleapis.com/calendar/v3/calendars/${calendarId}/events?key=${apiKey}&timeMin=${now}&orderBy=startTime&singleEvents=true`
        );
        const data = await response.json();
        displayEvents(data.items);
    } catch (error) {
        console.error("Error fetching events:", error);
        eventSection.innerHTML = "<p>Failed to load events.</p>";
    }
}

function displayEvents(events) {
    eventSection.innerHTML = ""; // Clear existing content

    if (!events || events.length === 0) {
        eventSection.innerHTML = "<p>No upcoming events.</p>";
        return;
    }

    events.forEach(event => {
        const eventDate = event.start.dateTime
            ? new Date(event.start.dateTime)  // Timed event
            : new Date(event.start.date);     // All-day event

        const eventElement = document.createElement("div");
        eventElement.classList.add("event-box");

        eventElement.innerHTML = `
            <div class="event-info">
                <h3>${event.summary}</h3>
                <p>${eventDate.toDateString()}</p>
                <a href="${event.htmlLink}" target="_blank">View on Google Calendar</a>
            </div>
        `;

        eventSection.appendChild(eventElement);
    });
}

// Fetch events when the page loads
fetchEvents();
