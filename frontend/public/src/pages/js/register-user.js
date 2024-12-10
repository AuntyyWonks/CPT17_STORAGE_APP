const registerUrl = "https://94yepvk88e.execute-api.eu-west-1.amazonaws.com/Prod/users";

document.getElementById('registerForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const name = document.getElementById('first_name').value;
    const surname = document.getElementById('last_name').value;
    const email = document.getElementById('email').value;
    
    const password1 = document.getElementById('password').value;
    const password2 = document.getElementById('confirm_password').value;
    const errorMessage = document.getElementById('error-message');

    const phoneNumber = document.getElementById('phone').value;

    errorMessage.style.display = 'none';
    errorMessage.textContent = '';

    if (password1 !== password2) {
        errorMessage.textContent = 'Passwords do not match.';
        errorMessage.style.display = 'block';
        return;
    }

    const newUserDetails = {
        name: name,
        surname: surname,
        email: email,
        phone_number: phoneNumber,
        password: password1
    };

    console.log(newUserDetails);

    try {
        fetch(registerUrl, {
            headers: {
                'Content-Type': 'application/json'
            },
            method: 'POST',
            body: JSON.stringify(newUserDetails),
        })
        .then(response => {
            if (response.ok) {
                console.log("Response: ");
                window.location.href = "login.html";
            } else {
                response.json().then( data => {
                    // Handle the error
                    errorMessage.textContent = data.error;
                    errorMessage.style.display = 'block';
                })
            }
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