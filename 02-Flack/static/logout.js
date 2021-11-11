/* Handles user logging out. */

// Remove username and last channel visited from local storage
if (localStorage.getItem('username')){
  console.log(`Removing user name: ${localStorage.getItem('username')}`)
  localStorage.removeItem('username');
}

if (localStorage.getItem('channel_name')){
  console.log(`Removing channel name: ${localStorage.getItem('channel_name')}`)
  localStorage.removeItem('channel');
}

// Clear everything (just in case)
localStorage.clear();
