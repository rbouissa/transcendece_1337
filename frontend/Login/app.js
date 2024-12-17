document.getElementById('loginForm').addEventListener('submit', async function (event) {
    event.preventDefault(); // Prevent default form submission

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    const data = { username, password };

    try {
        // Send login data to the Django backend API endpoint
        const response = await fetch('http://127.0.0.1:8000/api/login/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        });

        // Check if the response is OK (200-299 status codes)
        if (response.ok) {
            const responseData = await response.json();
            // Handle successful login (store token or session)
            alert('Login successful!');
        } else {
            const errorData = await response.json();
            document.getElementById('errorMessage').textContent = errorData.error;
        }
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('errorMessage').textContent = 'Network error. Please try again.';
    }
});


document.getElementById('intra42-login-btn').addEventListener('click', async () => {
    try {
        // Fetch the Intra42 authentication URL from the backend
        const response = await fetch('http://localhost:8000/api/login_with_42/', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        });

        if (response.ok) {
            // Extract the URL and redirect the user
            const data = await response.json();
            if (data.url) {
                window.location.href = data.url; // Redirect to Intra42 authentication page
            } else {
                console.error('URL not found in response');
            }
        } else {
            console.error('Failed to fetch authentication URL');
        }
    } catch (error) {
        console.error('Error during login:', error);
    }
});