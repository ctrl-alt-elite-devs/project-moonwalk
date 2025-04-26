console.log("Fetching Google Calendar Events...");

document.addEventListener("DOMContentLoaded", function () {
    const eventSection = document.getElementById("events");

    if (!eventSection) {
        console.error("Error: Element with id='events' not found!");
        return;
    }

    const calendarId = "e29b2d8a1f4a5d35f43f09f9fd7eecdb55b3c0ab9d66e16a8a76b54bb2772337@group.calendar.google.com";
    const apiKey = "AIzaSyDCC7xdWW8qCHxTULW5yAZSss5_AzcTj28";

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

            const uniqueEvents = removeDuplicateEvents(data.items); // Ensure no duplicates
            displayEvents(uniqueEvents);
        } catch (error) {
            console.error("Error fetching events:", error);
            eventSection.innerHTML = `<p>Error loading events: ${error.message}</p>`;
        }
    }

    function removeDuplicateEvents(events) {
        const uniqueEvents = [];
        const seenEvents = new Set();

        for (const event of events) {
            // Unique key: Combine ID, event name, and start date-time
            const eventKey = `${event.id}-${event.summary}-${event.start?.dateTime || event.start?.date}`;
            
            if (!seenEvents.has(eventKey)) {
                seenEvents.add(eventKey);
                uniqueEvents.push(event);
            } else {
                console.warn(`⚠ Duplicate event skipped: ${event.summary} on ${event.start?.dateTime || event.start?.date}`);
            }
        }

        return uniqueEvents;
    }

    function extractImgurImageLink(description) {
        if (!description) {
            console.warn("⚠ Event description is empty.");
            return null;
        }
    
        console.log(`Extracting image from description: ${description}`); // Debugging log
    
        // Updated regex to match Imgur links including .jpeg
        const imgurRegex = /(https?:\/\/i\.imgur\.com\/[a-zA-Z0-9]+\.jpg|https?:\/\/i\.imgur\.com\/[a-zA-Z0-9]+\.jpeg|https?:\/\/i\.imgur\.com\/[a-zA-Z0-9]+\.png|https?:\/\/i\.imgur\.com\/[a-zA-Z0-9]+\.gif)/;
        const match = description.match(imgurRegex);
    
        if (match && match[1]) {
            const extractedUrl = match[1];
            console.log(`✅ Extracted Imgur Image URL: ${extractedUrl}`); // Debugging log
            return extractedUrl;
        }
    
        console.warn("⚠ No valid Imgur image URL found in event description.");
        return null;
    }

    function displayEvents(events) {
        eventSection.innerHTML = ""; // Clear previous content

        if (!events || events.length === 0) {
            eventSection.innerHTML = "<p>No upcoming events.</p>";
            return;
        }

        for (const event of events.slice(0, 4)) {
            console.log(`Processing event: ${event.summary}`); // Debugging log

            if (!event.description) {
                console.warn(`⚠ Event "${event.summary}" has no description.`);
                continue;
            }

            console.log(`Event Description: ${event.description}`); // Debugging log

            const imgurImageLink = extractImgurImageLink(event.description);
            console.log(`Extracted Image URL: ${imgurImageLink}`); // Debugging log

            let eventDate, eventTime = "Unknown Time", endTime = "";

            if (event.start.dateTime) {
                // If it's a timed event
                eventDate = new Date(event.start.dateTime);
                const endDate = event.end?.dateTime ? new Date(event.end.dateTime) : null;

                eventTime = eventDate.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', hour12: true });

                if (endDate) {
                    endTime = ` - ${endDate.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', hour12: true })}`;
                }
            } else {
                // If it's an all-day event
                eventDate = new Date(event.start.date + "T00:00:00");
                eventDate.setMinutes(eventDate.getMinutes() + eventDate.getTimezoneOffset());
                eventTime = "All Day";
            }

            let eventElement = document.createElement("div");
            eventElement.classList.add("event-box");

            const imageTag = imgurImageLink ? `<img src="${imgurImageLink}" alt="Event Image" style="max-width:100%; height:auto; margin-bottom: 10px;">` : "";

            eventElement.innerHTML = `
                ${imageTag}
                <p class="event-description">
                    <strong>Name:</strong> ${event.summary}<br>
                    <strong>Date:</strong> ${eventDate.toDateString()}<br>
                    <strong>Time:</strong> ${eventTime}${endTime}<br>
                    <a href="${event.htmlLink}" target="_blank" class="calendar-link">View on Google Calendar</a>
                </p>
            `;

            eventSection.appendChild(eventElement);
        }
    }

    // Fetch events when the page loads
    fetchEvents();
});
