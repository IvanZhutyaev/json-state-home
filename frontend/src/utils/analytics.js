const userId = localStorage.getItem("user_id") || crypto.randomUUID();
localStorage.setItem("user_id", userId);

export function sendEvent(apartmentId, eventType, value = null) {
  fetch("https://yourdomain.com/api/track-event", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      apartment_id: apartmentId,
      user_id: userId,
      event_type: eventType,
      event_value: value
    })
  });
} 