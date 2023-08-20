import random
import string

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError

from datetime import datetime, timedelta
from phone_field import PhoneField


CHARACTERISATIONS = [
    "nature", "cultural", "food", "adventurous", "nightlife", "romantic", "relaxing",
    "shopping"
]

class User(AbstractUser):
    pass


class Country(models.Model):
    """Southeast Asia countries"""
    country = models.CharField(blank=False, max_length=265)

    # starting and returning point for each day when itinerary is planned
    # temporary solution since planner not taking in hotel location yet
    datum_pt_longitude = models.FloatField(
        blank=False, null=False,
        validators=[MaxValueValidator(90), MinValueValidator(-90)]
    )
    datum_pt_latitude = models.FloatField(
        blank=False, null=False,
        validators=[MaxValueValidator(90), MinValueValidator(-90)]
    )

    def __str__(self):
        return self.country


class Budget(models.Model):
    """Three budget types"""
    budget = models.CharField(blank=False, max_length=265)

    def __str__(self):
        return self.budget


class Period(models.Model):
    """Time to spend at one attraction"""
    period = models.FloatField(blank=False, null=False)

    def __str__(self):
        return "{}".format(self.period)


class Category(models.Model):
    """Attraction Category"""
    category = models.CharField(blank=False, null=False, max_length=300)
    period = models.ForeignKey(Period, on_delete=models.CASCADE)

    def __str__(self):
        return self.category


class Planner(models.Model):
    """Planner"""
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)

    # basic stuff
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    people = models.IntegerField(
        default=1,
        validators=[MaxValueValidator(6), MinValueValidator(1)]
    )
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE)
    start_date = models.DateField(blank=False)
    end_date = models.DateField(blank=False)
    date_created = models.DateTimeField(blank=False)

    # characterisation
    nature = models.BooleanField(blank=False, null=False)
    cultural = models.BooleanField(blank=False, null=False)
    food = models.BooleanField(blank=False, null=False)
    adventurous = models.BooleanField(blank=False, null=False)
    nightlife = models.BooleanField(blank=False, null=False)
    romantic = models.BooleanField(blank=False, null=False)
    relaxing = models.BooleanField(blank=False, null=False)
    shopping = models.BooleanField(blank=False, null=False)

    # random string
    rand_key = models.CharField(blank=False, null=False, max_length=10)

    def __str__(self):
        return "{}_{}_{}_{}".format(
            self.country,
            self.start_date,
            self.end_date,
            self.user
        )


    def get_no_of_days(self):
        """Find out total number of days"""
        return self.end_date - self.start_date + timedelta(days=1)


    @property
    def characterisation_scores(self):
        """Return all scores as a dictionary"""
        return {
            "nature": self.nature,
            "cultural": self.cultural,
            "food": self.food,
            "adventurous": self.adventurous,
            "nightlife": self.nightlife,
            "romantic": self.romantic,
            "relaxing": self.relaxing,
            "shopping": self.shopping,
        }

    def clean(self):
        """Validate input"""
        # start data cannot be in the past
        if self.start_date < datetime.date(datetime.now()):
            raise ValidationError(
                "Start date {} cannot be in the past".format(
                    self.start_date)
            )

        # end date needs to be greater than start date
        if self.start_date > self.end_date:
            raise ValidationError(
                "End date {} has to be either the same or after start date".format(
                    self.end_date)
            )

    def save(self, *args, **kwargs):
        try:
            self.full_clean()
        except ValidationError as e:
            return e.messages
        return super(Planner, self).save(*args, **kwargs)

    @staticmethod
    def get_random_string(length=10):
        """Generate random string with a specific length."""
        letters = string.ascii_lowercase
        result_str = ''.join(random.choice(letters) for i in range(length))
        return result_str

    def get_planner_interest(self):
        """Return a list of characterisation that interests the user"""
        interest = []
        for x in CHARACTERISATIONS:
            if getattr(self, x) is True:
                interest.append(x)
        return interest

    def get_unique_itinerary_key(self):
        """Return key to access Itinerary model"""
        return "{}_{}".format(self.rand_key, self.id)


class Attraction(models.Model):
    """Attraction model"""
    # compulsory items
    name = models.CharField(blank=False, null=False, max_length=300)
    address = models.TextField(blank=False, null=False)
    origin = models.BooleanField(blank=False, null=False, default=False)  # origin of a country
    country = models.ForeignKey(
        Country, on_delete=models.CASCADE, blank=False, null=False
    )
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, blank=False, null=False
    )
    budget = models.ForeignKey(
        Budget, on_delete=models.CASCADE, blank=False, null=False
    )
    nature = models.BooleanField(blank=False, null=False)
    cultural = models.BooleanField(blank=False, null=False)
    food = models.BooleanField(blank=False, null=False)
    adventurous = models.BooleanField(blank=False, null=False)
    nightlife = models.BooleanField(blank=False, null=False)
    romantic = models.BooleanField(blank=False, null=False)
    relaxing = models.BooleanField(blank=False, null=False)
    shopping = models.BooleanField(blank=False, null=False)
    longitude = models.FloatField(
        blank=False, null=False,
        validators=[MaxValueValidator(90), MinValueValidator(-90)]
    )
    latitude = models.FloatField(
        blank=False, null=False,
        validators=[MaxValueValidator(90), MinValueValidator(-90)]
    )

    # optional items
    rating = models.FloatField(blank=True, null=True)
    phone = PhoneField(blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    photo_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return "{}_{}_{}".format(
            self.name, self.country, self.budget
        )

    @property
    def period(self):
        return self.category.period.period


class Itinerary(models.Model):
    """Itinerary model"""
    planner = models.ForeignKey(Planner, on_delete=models.CASCADE)
    day = models.IntegerField(blank=False, null=False)
    attraction = models.ForeignKey(Attraction, on_delete=models.CASCADE)

    @property
    def period(self):
        return self.planner.category.period
