from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("start", views.get_start_page, name="start"),
    path("itinerary/<str:key>", views.show_itinerary, name="itinerary"),
    path("userprofile", views.view_profile, name="userprofile"),

    #API Routes
    path("register", views.register, name="register"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("planmytrip", views.plan_my_trip, name="planmytrip"),
    path("attraction/<int:attraction_id>", views.show_attraction, name="attraction"),
    path("useremail", views.get_login_user_email, name="useremail"),
]
