document.addEventListener('DOMContentLoaded', function() {

    // toggle between views on home page
    document.querySelector('#home').addEventListener('click', () => scroll_page('home'));
    document.querySelector('#seaInfo').addEventListener('click', () => scroll_page('sea'));
    document.querySelector('#aboutUs').addEventListener('click', () => scroll_page('about-us'));

    // toggle to see countries in SEA
    document.querySelector('#left-country-btn').addEventListener('click', () => toggle_country('left'));
    document.querySelector('#right-country-btn').addEventListener('click', () => toggle_country('right'));
});

function scroll_page(page_name){
    // scroll to correct page when menu bar button is clicked
    var element = document.getElementById(`${page_name}-view`);

    // need to offset height pass the fixed menu bar at the start of the page
    const yOffset = document.body.scrollHeight * 0.02;
    const y = element.getBoundingClientRect().top + window.pageYOffset - yOffset;
    window.scrollTo({top: y, behavior: 'smooth'});
};

function toggle_country(direction){
    // switch to show a different country when button is pressed
    ele = document.getElementsByClassName("country-info")[0]
    var country_id = parseInt(ele.id);

    if (direction == 'left'){
        country_id = country_id - 1;
    } else {
        country_id = country_id + 1;
    };

    if (country_id == -1){
        country_id = 10;
    };

    if (country_id == 11){
        country_id = 0;
    };

    const countries = [
        "Brunei",
        "Burma",
        "Cambodia",
        "Timor-Leste",
        "Indonesia",
        "Laos",
        "Malaysia",
        "Philippines",
        "Singapore",
        "Thailand",
        "Vietnam"
    ]

    // load new picture and update heading and id
    var country = countries[country_id];
    document.getElementsByClassName("flag-img")[0].src=`/static/trip/images/${country}.png`;
    ele.id = country_id;
    document.querySelector("#country-name").innerHTML = country
};
