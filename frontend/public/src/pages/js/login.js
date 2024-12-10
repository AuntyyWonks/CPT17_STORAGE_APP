const loginUrl = "https://94yepvk88e.execute-api.eu-west-1.amazonaws.com/Prod/login";

document.getElementById('loginForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const errorMessage = document.getElementById('error-message');

    errorMessage.style.display = 'none';
    errorMessage.textContent = '';

    const userDetails = {
        username: username,
        password: password
    };

    console.log(userDetails);

    try {
        fetch(loginUrl, {
            headers: {
                'Content-Type': 'application/json'
            },
            method: 'POST',
            body: JSON.stringify(userDetails),
        })
        .then(response => {
            response.json().then( data => {
                if (response.ok) {
                    localStorage.setItem('id_token', data.id_token);
                    localStorage.setItem('access_token', data.access_token);
                    localStorage.setItem('refresh_token', data.refresh_token);
                    
                    window.location.href = "homeconsole.html";
                } else {
                    // Handle the error
                    errorMessage.textContent = data.error;
                    errorMessage.style.display = 'block';
                }
                
            })
            
        })
        .catch(error => {
            console.error("There was a problem with the fetch ", error);
        });
    } catch (err) {
        console.log(err);
        errorMessage.textContent = err;
        errorMessage.style.display = 'block';
    }
});