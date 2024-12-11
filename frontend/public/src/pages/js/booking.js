const bookingUrl = "https://94yepvk88e.execute-api.eu-west-1.amazonaws.com/Prod/bookings";

document.getElementById('bookingForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const town = document.getElementById('town').value;
    const unitSize = sessionStorage.getItem("unitSize");
    const errorMessage = document.getElementById('error-message');

    errorMessage.style.display = 'none';
    errorMessage.textContent = '';

    const bookingDetails = {
        townId: town,
        unitSize: unitSize
    };

    console.log(bookingDetails);

    try {
        fetch(bookingUrl, {
            headers: {
                'Content-Type': 'application/json',
                'Authorization': localStorage.getItem("id_token")
            },
            method: 'POST',
            body: JSON.stringify(bookingDetails),
        })
        .then(response => {
            response.json().then( data => {
                if (response.ok) {
                    console.log("response: ");
                    console.log(response);
                     window.location.href = "viewstorage.html";
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