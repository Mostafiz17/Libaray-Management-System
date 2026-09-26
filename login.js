const API_URL = 'http://127.0.0.1:8000';
const form = document.querySelector('#login-form'); const message = document.querySelector('#message');
if (localStorage.getItem('access_token')) window.location.href = 'books.html';
form.addEventListener('submit', async (event) => { event.preventDefault(); const button=form.querySelector('button'); button.disabled=true; message.textContent='';
  const body = new URLSearchParams({ username: document.querySelector('#email').value.trim(), password: document.querySelector('#password').value });
  try { const response=await fetch(`${API_URL}/auth/login`, {method:'POST',headers:{'Content-Type':'application/x-www-form-urlencoded'},body}); const data=await response.json(); if(!response.ok) throw new Error(data.detail || 'Unable to sign in.'); localStorage.setItem('access_token',data.access_token); window.location.href='books.html'; }
  catch(error){ message.textContent=error.message.includes('Failed to fetch')?'Could not reach the API. Is FastAPI running?':error.message; message.className='message error'; button.disabled=false; }
});
