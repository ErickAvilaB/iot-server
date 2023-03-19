// File to main page

// Button to change led state
const button = document.getElementById('toggle');

// Data to send to server
let id = 1;
let ledState = 0;

// Make put request to server
button.addEventListener('click', async () => {
  ledState = ledState ? 0 : 1;

  // Data to send to server
  let data = {
    id: 1,
    state: ledState,
  };

  // Request options
  let options = {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  };

  await fetch('http://localhost:5000/put_state', options);
});
