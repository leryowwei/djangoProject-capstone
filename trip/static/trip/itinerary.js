document.addEventListener('DOMContentLoaded', function() {

});

const all_fields = [
    "name", "address", "phone", "url", "budget", "category", "rating",
]

function view_attraction(attraction_id){
    // send out data
    fetch(`/attraction/${attraction_id}`, {
        method: 'GET',
    })
    .then(response => response.json())
    .then(result => {
        console.log(result);

        var explain_container = document.getElementById("itinerary-explain-container");
        var table_container = document.getElementById("itinerary-table-container");

        explain_container.style.width = "40%";
        explain_container.style.transition = "width 1s";
        table_container.style.width = "60%";
        table_container.style.transition = "width 1s";
        explain_container.style.visibility = "visible";
        table_container.style.transition = "visibility 0.5s";

        const attraction = result["result"];

        // name
        document.getElementById("attraction-name").innerHTML = attraction["name"];

        // address
         document.getElementById("attraction-address").innerHTML = attraction["address"];

        // budget
        document.getElementById("attraction-budget").innerHTML = `${attraction["budget"]} Location`;

        // category and period
        document.getElementById("attraction-category").innerHTML = `${attraction["category"]}`;
        document.getElementById("attraction-period").innerHTML = `Spend ${attraction["period"]} hour(s)`;

        // rating
        var ele = document.getElementById("attraction-rating");

        if (attraction["rating"] == null){
            ele.style.display = "none";
            ele.innerHTML = "";
        } else{
            ele.style.display = "block";
            ele.innerHTML = `Rating: ${attraction["rating"]}`;
        };

        // phone
        var ele = document.getElementById("attraction-phone");

        if (attraction["phone"] == null){
            ele.style.display = "none";
            ele.innerHTML = "";
        } else{
            ele.style.display = "block";
            ele.innerHTML = `Phone: ${attraction["phone"]} | `;
        };

        // url
        var ele = document.getElementById("attraction-url");

        if (attraction["url"] == null){
            ele.style.display = "none";
            ele.innerHTML = "";
        } else{
            ele.style.display = "block";
            ele.setAttribute("href", attraction["url"]);
            ele.innerHTML = "Visit website"
        };

        // photo
        var ele = document.getElementById("attraction-photo-container");

        if (attraction["photo_url"] == null){
            ele.style.display = "none";
        } else{
            ele.style.display = "block";
            document.getElementById("attraction-photo").setAttribute("src", attraction["photo_url"]);
        };

        // description
        var ele = document.getElementById("attraction-description");

        if (attraction["description"] == null){
            ele.style.display = "none";
            ele.innerHTML = "";
        } else{
            ele.style.display = "block";
            ele.innerHTML = attraction["description"];
        };

    })
    // Catch any errors and log them to the console
    .catch(error => {
        console.log('ERROR:', error);
    });
};
