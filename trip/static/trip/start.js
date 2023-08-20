const sea_countries = [
    "Brunei", "Burma", "Cambodia", "Indonesia", "Laos", "Malaysia", "Philippines", "Singapore",
    "Thailand", "Timor-Leste", "Vietnam"
];

const budget_options = ["Budget", "Normal", "Premium"];

const characterisation_options = ["nature", "cultural", "food", "adventurous", "nightlife", "romantic", "relaxing", "shopping"];

document.addEventListener('DOMContentLoaded', function() {
    const url_hash = window.location.hash;

    if (url_hash){
        toggle_option(url_hash);
    };
});


async function toggle_option(option){
    /** display fields depending on whether user chooses login, sign up or continue option */
    var ele = document.querySelector("#login-sign-up");

    const url = new URL(window.location);

    if (option == "#login"){
        ele.innerHTML =
            '<h1>Login</h1>' +
            '<input type="email" id="login-email" placeholder="Email Address" required><br>' +
            '<input type="password" id="login-password" placeholder="Password" required><br>' +
            '<button class="btn btn-lg base-btn" id="btn-confirm-sign-in">Sign In</button><br>' +
            '<span id="error"></span><br>';
        document.querySelector('#btn-confirm-sign-in').addEventListener('click', (event) => confirm_sign_in(event));
        url.hash = '#login';
    } else if (option == "#signup"){
        ele.innerHTML =
            '<h1>Sign Up</h1>' +
            '<input type="text" id="sign-up-first-name" placeholder="First Name" required><br>' +
            '<input type="text" id="sign-up-last-name" placeholder="Last Name" required><br>' +
            '<input type="email" id="sign-up-email" placeholder="Email Address" required><br>' +
            '<input type="password" id="sign-up-password" placeholder="Password" required><br>' +
            '<input type="password" id="sign-up-password-confirm" placeholder="Retype Password" required><br>' +
            '<button type="submit" class="btn btn-lg base-btn" id="btn-confirm-sign-up">Sign up</button><br>'+
            '<span id="error"></span>';
        document.querySelector('#btn-confirm-sign-up').addEventListener('click', (event) => confirm_sign_up(event));
        url.hash = '#signup';
    } else if (option == "#continue"){
        await toggle_planner();
        url.hash = '#continue';
    };

    // change div width to show these options
    document.querySelector("#prompt").style.width = "40%";
    document.querySelector("#prompt").style.transition = "width 1.5s";
    ele.style.width = "60%";
    ele.style.transition = "width 1.5s";

    window.history.pushState({}, '', url);
};

async function toggle_planner(){
    /** show planner tool to allow user to input their itinerary */
    var ele = document.querySelector("#login-sign-up");

    // get user email address
    const user = await get_user_email();

    console.log(user);

    // clear html
    ele.innerHTML = "";

    // add header and login details
    var header_container = document.createElement("div");
    header_container.className = "header-container";
    header_container.appendChild(create_element("div", {"class": "header"}, "Planner"));

    // add login details if user is signed in
    var img_container = document.createElement("div");
    img_container.className = "img-container";
    img_container.appendChild(create_element("img", {"class": "login-img", "src": "static/trip/images/login.png"}));
    if (user != ""){
        img_caption = create_element("div", {"class": "img-caption", "id": user}, `Login as ${user}`);
    } else{
        img_caption = create_element("div", {"class": "img-caption", "id": ""}, 'Continue as guest');
    };
    img_container.appendChild(img_caption);
    header_container.appendChild(img_container);
    ele.appendChild(header_container);

    // add countries
    var dict = {"list": "countries", "id": "country", "required": "",  "placeholder": "country"};
    ele.appendChild(create_element("input", dict));
    ele.appendChild(create_datalist(sea_countries, "countries"));

    // start date and end date
    var date_container = document.createElement("div");
    date_container.className = "date-container";
    const dates = ['start date', 'end date'];
    for (const option of dates){
        var input = document.createElement("input");
        input.className = "date-input"
        input.addEventListener("focus", function(){this.type='date'});
        input.addEventListener("focusout", function(){this.type='text'});
        input.placeholder = option;
        input.id = option.replace(" ", "-");
        date_container.appendChild(input);
    };
    ele.appendChild(date_container);

    // no of people + budget
    var container = document.createElement("div");
    container.className = "people-budget-container";
    var dict = {"type": "number", "id": "people", "min": "1", "max": "6", "required": "", "placeholder": "number of people"};
    container.appendChild(create_element("input", dict));
    var dict = {"list": "budgets", "id": "budget", "required": "",  "placeholder": "budget"};
    container.appendChild(create_element("input", dict));
    container.appendChild(create_datalist(budget_options, "budgets"));
    ele.appendChild(container);

    // characterisation scores
    var characterisation_container = document.createElement("div");
    characterisation_container.className = "characterisation-container";
    var scales_header = document.createElement("h5");
    scales_header.innerHTML = "Personalise your trip";
    scales_header.className = "characterisation-header";
    characterisation_container.appendChild(scales_header);
    for (const option of characterisation_options){
        var container = document.createElement("div");
        var dict = {"for": option, "class": "characterisation-label"};
        container.appendChild(create_element("label", dict, `${option.capitalize()} : &nbsp;`));
        var dict = {"type": "checkbox", "id": option};
        container.appendChild(create_element("input", dict));
        characterisation_container.appendChild(container);
    };
    ele.appendChild(characterisation_container);

    // submit button
    var button_container = document.createElement("div");
    button_container.className = "button-container";
    var dict = {"class": "btn btn-lg base-btn", "id": "btn-planner-submit"};
    btn = create_element("button", dict, "Plan my trip!");
    btn.addEventListener('click', (event) => plan_my_trip(event));
    button_container.appendChild(btn);
    ele.appendChild(button_container);

    // add error bar
    ele.appendChild(create_element("span", {"id": "error"}));
};


function confirm_sign_up(event){
    /** POST sign up details to register and sign in user*/
    const form = document.getElementById("login-sign-up");
    const isValid = form.reportValidity();

    var ele = document.querySelector("#error");
    ele.textContent = "";

    if (isValid) {
        event.preventDefault();

        // send out data
        fetch('register', {
            method: 'POST',
            body: JSON.stringify({
                first_name: document.getElementById("sign-up-first-name").value,
                last_name: document.getElementById("sign-up-last-name").value,
                email: document.getElementById("sign-up-email").value,
                password: document.getElementById("sign-up-password").value,
                password_confirmation: document.getElementById("sign-up-password-confirm").value,
            })
        })
        .then(response => response.json())
        .then(result => {
            // Print result
            event.preventDefault();
            console.log(result);

            // display error on page for user
            if(("error" in result)){
                ele.textContent = result["error"];
                ele.style.color = "red";
                ele.style.height = "2vh";
            } else {
                // refresh page
                removeHash();
                window.location.pathname = "/start";
            };
        })
        // Catch any errors and log them to the console
        .catch(error => {
            console.log('ERROR:', error);
        });
    }
};


function confirm_sign_in(event){
    /** Post sign in details to login user */
    const form = document.getElementById("login-sign-up");
    const isValid = form.reportValidity();

    var ele = document.querySelector("#error");
    ele.textContent = "";

    if (isValid) {

        event.preventDefault();

        // read from input
        email_add = document.getElementById("login-email").value;
        password = document.getElementById("login-password").value;

        // send out data
        fetch('login', {
            method: 'POST',
            body: JSON.stringify({
                email: email_add,
                password: password,
            })
        })
        .then(response => response.json())
        .then(result => {
            // Print result
            event.preventDefault();
            console.log(result);

            // display error on page for user
            if(("error" in result)){
                ele.textContent = result["error"];
                ele.style.color = "red";
                ele.style.height = "2vh";
            } else {
                // refresh page again
                removeHash();
                location.reload();
            };
        })
        // Catch any errors and log them to the console
        .catch(error => {
            console.log('ERROR:', error);
        });
    }
};


function plan_my_trip(event){
   /** POST itinerary details to server*/
   const form = document.getElementById("login-sign-up");
   const isValid = form.reportValidity();

   var ele = document.querySelector("#error");
   ele.textContent = "";

   document.body.className = 'waiting';

   if (isValid) {
       event.preventDefault();

       // send out data
       fetch('planmytrip', {
           method: 'POST',
           body: JSON.stringify({
               country: document.getElementById("country").value,
               start_date: document.getElementById("start-date").value,
               end_date: document.getElementById("end-date").value,
               people: document.getElementById("people").value,
               budget: document.getElementById("budget").value,
               nature: document.getElementById("nature").checked,
               cultural: document.getElementById("cultural").checked,
               food: document.getElementById("food").checked,
               adventurous: document.getElementById("adventurous").checked,
               nightlife: document.getElementById("nightlife").checked,
               romantic: document.getElementById("romantic").checked,
               relaxing: document.getElementById("relaxing").checked,
               shopping: document.getElementById("shopping").checked,
           })
       })
       .then(response => response.json())
       .then(result => {
           // Print result
           event.preventDefault();
           console.log(result);

           // display error on page for user
           if(("error" in result)){
               ele.textContent = result["error"];
               ele.style.color = "red";
               ele.style.height = "2vh";
           } else {
               toggle_itinerary(result["planner_key"], result["planner_id"]);
           };
       })
       // Catch any errors and log them to the console
       .catch(error => {
           console.log('ERROR:', error);
       });
   } else{
       console.log("dumb");
       document.body.className = '';
   };
};


function toggle_itinerary(planner_key, planner_id){
    window.location.pathname = `itinerary/${planner_key}_${planner_id}`;
    window.location.hash = "";
};


function log_out(){
    /** Logout current user sessions */
    fetch('logout', {
        method: 'POST',
    })
    .then(response => response.json())
    .then(result => {
        console.log(result["result"]);
        window.location.pathname = "";
    })
    // Catch any errors and log them to the console
    .catch(error => {
        console.log('ERROR:', error);
    });
};

function view_profile(){
    /** Load profile page */
    removeHash();
    window.location.pathname = "/userprofile";
};


async function get_user_email() {
    /** Fetch user email address via api; */
    try {
        const response = await fetch("useremail");
        const users = await response.json();
        return users["email"];
     } catch(err){
        console.error(err);
     };
};


function create_datalist(options, id_name){
    /** Helper function to create datalist based on input */
    var datalist = document.createElement("datalist");
    datalist.id = id_name;
    for (const x of options){
        var option = document.createElement("option");
        option.value = x;
        datalist.appendChild(option);
    };

    return datalist;
};

function create_element(ele_name, dict, text = ""){
    /** Helper function to create element field */
    var element = document.createElement(ele_name);
    for (var key in dict){
        element.setAttribute(key, dict[key]);
    };

    if (text != ""){
        element.innerHTML = text;
    };

    return element;
};

function removeHash () {
    var scrollV, scrollH, loc = window.location;
    if ("pushState" in history)
        history.pushState("", document.title, loc.pathname + loc.search);
    else {
        // Prevent scrolling by storing the page's current scroll offset
        scrollV = document.body.scrollTop;
        scrollH = document.body.scrollLeft;

        loc.hash = "";

        // Restore the scroll offset, should be flicker free
        document.body.scrollTop = scrollV;
        document.body.scrollLeft = scrollH;
    }
}


Object.defineProperty(String.prototype, 'capitalize', {
    value: function() {
      return this.charAt(0).toUpperCase() + this.slice(1);
    },
    enumerable: false
  });