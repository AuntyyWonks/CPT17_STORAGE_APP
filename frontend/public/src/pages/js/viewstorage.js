const bookedUnitsUrl = "https://94yepvk88e.execute-api.eu-west-1.amazonaws.com/Prod/bookings";


function checkStorage() {
    const userDetails = {
        username: localStorage.getItem("username")
    };

    console.log(userDetails);
    try {
        fetch(bookingUrl, {
            headers: {
                'Content-Type': 'application/json'
            },
            method: 'GET',
            body: JSON.stringify(userDetails),
        })
        .then(response => {
            response.json().then( data => {
                if (response.ok) {
                    console.log(data);

                    unitsBooked = data.body;

                    // update table with data
                    myUnits = document.getElementById("my-units");

                    var table = document.createElement("TABLE");
                    table.setAttribute("id", "myTable");
                    myUnits.appendChild(table);

                    for (var i = 0; i < unitsBooked.length; i++) {
                        var unitBooked = unitsBooked[i];
                        var row = document.createElement("TR");
                    
                        var townCell = document.createElement("TD");
                        var unitSizeCell = document.createElement("TD");
                        var statusCell = document.createElement("TD");
                    
                        row.appendChild(townCell);
                        row.appendChild(unitSizeCell);
                        row.appendChild(statusCell);
                    
                        var town = document.createTextNode(unitBooked.townID);
                        var unitSize = document.createTextNode(unitBooked.unitSize);
                        var status = document.createTextNode(unitBooked.status);
                    
                        townCell.appendChild(town);
                        unitSizeCell.appendChild(unitSize);
                        statusCell.appendChild(status);
                    
                        table.appendChild(row);
                        document.body.appendChild(document.createElement('hr'));
                    }
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
}
window.onload = checkStorage;