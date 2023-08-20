import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Itinerary, User, Planner, Country, Budget, Attraction
from .planner import plan_trip
from datetime import datetime


def index(request):
    """Home page"""
    return render(request, "trip/index.html")

def get_start_page(request):
    """Start page"""
    return render(request, "trip/start.html")


@csrf_exempt
def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        data = json.loads(request.body)
        email = data["email"]
        password = data["password"]
        user = authenticate(username=email, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return JsonResponse({"result": "Login successful."}, status=201)
        else:
            return JsonResponse({"error": "Invalid email/ passsword."}, status=404)


@csrf_exempt
def logout_view(request):
    """Logout current user session"""
    if request.method == "POST":
        logout(request)
        return JsonResponse({"result": "Logout successful."}, status=201)


@csrf_exempt
def register(request):
    """Register profile"""
    if request.method == "POST":
        data = json.loads(request.body)
        first_name = data["first_name"]
        last_name = data["last_name"]
        email = data["email"]

        # Ensure password matches confirmation
        password = data["password"]
        confirmation = data["password_confirmation"]
        if password != confirmation:
            return JsonResponse({"error": "Passwords must match."}, status=404)
        # Attempt to create new user
        try:
            user = User.objects.create_user(
                username=email, email=email, first_name=first_name, last_name=last_name, password=password
            )
            user.save()
        except IntegrityError as e:
            print(e)
            return JsonResponse({"error": "Account already exists for the email address."}, status=404)
        login(request, user)
        return JsonResponse({"result": "Account created."}, status=201)


@csrf_exempt
def plan_my_trip(request):
    """Plan trip based on user input"""
    if request.method == "POST":
        data = json.loads(request.body)

        # get user object if is login. Otherwise assign to guest
        if request.user.is_authenticated:
            user = User.objects.get(username = request.user.username)
        else:
            user = User.objects.get(username = "guest")

        # get country object
        try:
            country = Country.objects.get(country = data["country"])
        except ObjectDoesNotExist:
            return JsonResponse(
                {"error": "Country {} does not exist".format(data["country"])},
                status=404
            )

        # get budget object
        try:
            budget = Budget.objects.get(budget = data["budget"])

        except ObjectDoesNotExist:
            return JsonResponse(
                {"error": "Budget {} does not exist".format(data["budget"])},
                status=404
            )

        # before creating planner object, check that we actually have attractions data
        # for that specific country. Otherwise, we can't start planning.
        # set the limit to 10 places for now
        if len(Attraction.objects.filter(country=country)) < 10:
            msg = (
                "Unfortunately, we do not have enough data for {}"
                " to start planning a trip for you. Please choose another country."
            ).format(country)

            return JsonResponse({"error": msg}, status=404)

        # create itinerary planner model
        planner = Planner.objects.create(
            user = user,
            country = country,
            start_date = datetime.strptime(data["start_date"], "%Y-%m-%d").date(),
            end_date = datetime.strptime(data["end_date"], "%Y-%m-%d").date(),
            date_created = datetime.now(),
            people = data["people"],
            budget = budget,
            nature = data["nature"],
            cultural = data["cultural"],
            food = data["food"],
            adventurous = data["adventurous"],
            nightlife = data["nightlife"],
            romantic = data["romantic"],
            relaxing = data["relaxing"],
            shopping = data["shopping"],
            rand_key = Planner.get_random_string(),
        )

        # clean and save data. Return error message if validationerror occured
        e = planner.save()
        if e:
            return JsonResponse({"error": e}, status=404)
        else:
            plan_trip(planner)
            # passing back a randomly generated key rather than a easily predicted id
            return JsonResponse(
                {"planner_key": planner.rand_key, "planner_id": planner.id}, status=201
            )

def show_itinerary(request, key):
    """Show itinerary"""
    rand_key, id = key.split("_")
    planner =  Planner.objects.get(rand_key=rand_key, id=id)
    itinerary = Itinerary.objects.filter(planner = planner)

    attractions = {}

    max_length = 0

    for attraction in itinerary:
        if attraction.day not in attractions:
            attractions[attraction.day] = [attraction.attraction]
        else:
            attractions[attraction.day].append(attraction.attraction)

        if len(attractions[attraction.day]) > max_length:
            max_length = len(attractions[attraction.day])

    if planner.get_planner_interest():
        characterisation = ", ".join([x.capitalize() for x in planner.get_planner_interest()])
    else:
        characterisation = None

    return render(
        request, "trip/itinerary.html", {
            "itinerary": attractions,
            "range": range(1, max_length + 1),
            "planner": planner,
            "characterisation": characterisation,
        }
    )


def show_attraction(request, attraction_id):
    """Show information of an attraction"""
    if request.method == "GET":
        attraction = Attraction.objects.get(id=attraction_id)

        # unpack model data as a nice dictionary
        result = {
            "name": attraction.name,
            "budget": attraction.budget.budget,
            "category": attraction.category.category,
            "period": attraction.period,
            "address": attraction.address,
            "url": attraction.url,
            "rating": attraction.rating,
            "description": attraction.description,
            "photo_url": attraction.photo_url,
        }

        if attraction:
            return JsonResponse({"result": result}, status=201)
        else:
            return JsonResponse({"error": "Model not found."}, status=404)


@login_required
def view_profile(request):
    """View profile page for the logged in user"""

    if request.user.is_authenticated:
        user = User.objects.get(username = request.user.username)
        planner_list = Planner.objects.filter(user=user)
        planner_list = planner_list.order_by("-date_created")
        page = request.GET.get('page', 1)
        paginator = Paginator(planner_list, 5)

        try:
            planner = paginator.page(page)
        except PageNotAnInteger:
            planner = paginator.page(1)
        except EmptyPage:
            planner = paginator.page(paginator.num_pages)


        return render(
            request, "trip/profile.html", {
                "user": user,
                "planner": planner,
            }
        )
    else:
        return HttpResponseBadRequest("User needs to be logged in to view profile page!")


@csrf_exempt
def get_login_user_email(request):
    """Return user email address if already login"""
    if request.user.is_authenticated:
        # username is email
        return JsonResponse({"email": request.user.username}, status=201)
    else:
        # return empty string if not login
        return JsonResponse({"email": ""}, status=201)
