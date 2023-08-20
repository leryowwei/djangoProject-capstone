"""Itinerary planner algorithm"""

import copy
import math
import numpy as np
import random

from trip.models import Country, Attraction, Itinerary

# --- constants ---

# period = hr
# distance = (0,1) or (1,0)
PERIOD_PER_DAY = 8
PERIOD_PER_DISTANCE = 0.5

# 4 hours after start of day
LUNCH_TIME = 4

# q model iteration
iterations = 75000

# Hyperparameters
ALPHA = 0.3
GAMMA = 0.6
EPSILON = 0.1

# reward
REWARD = {
    "budget": 20,
    "characterisation": 500,
    "lunch": 1000,
    "ratings": 10,
}

# penalty
PENALTY = {
    "budget": -50,
    "distance": -10,
    "exceed_period_per_day": -10000,
    "same_location": -10000,
    "restaurant": -3000,
    "ratings": -10,
}


def initialisation():
    restaurants_category = [
        "restaurant", 'french', 'scandinavian', 'asian', 'australian', 'food court',
        'south indian', 'Seafood', 'Snacks', 'Beer Garden', 'Indian', 'Noodles',
        'Malay', 'Bakery', 'Food & Drink', 'Chinese', 'Dim Sum', 'Coffee Shop', 'Diner',
    ]
    restaurants_category = [x.lower() for x in restaurants_category]
    country = Country.objects.get(country="Singapore")
    attractions = Attraction.objects.filter(country=country)
    no_of_attractions = len(attractions)
    q_table = np.zeros((no_of_attractions, no_of_attractions, PERIOD_PER_DAY))
    attractions_id = [x.id for x in attractions]
    restaurants_id = [x.id for x in attractions if x.category.category.lower() in restaurants_category]
    st = set(restaurants_id)
    restaurant_indices = [i for i, e in enumerate(attractions_id) if e in st]

    return q_table, no_of_attractions, attractions, restaurant_indices


def calculate_distance(origin_x, origin_y, des_x, des_y):
    """Calculate distance between two points"""
    return math.sqrt(math.pow(des_x - origin_x, 2) + math.pow(des_y - origin_y, 2))


def calculate_rewards(df_origin, df_destination, origin_index, des_index, curr_time, restaurant_indices, user_characterisations, user_budget):
    """Calulate net rewards (reward - penalty)"""
    net_reward = 0

    # based on budget
    des_budget = df_destination.budget.id
    if des_budget <= user_budget:
        net_reward += REWARD["budget"] * abs(user_budget - des_budget)
    else:
        net_reward += PENALTY["budget"] * abs(user_budget - des_budget)

    # based on distance
    distance = calculate_distance(df_origin.latitude, df_origin.longitude, df_destination.latitude, df_destination.longitude)
    net_reward += PENALTY["distance"] * distance

    # based on characertisation scores
    # reward if the venue aligns more with what the traveller wants
    for characterisation, value in user_characterisations.items():
        if value == getattr(df_destination, characterisation):
            net_reward += REWARD["characterisation"]

    # penalise if travel to the same location again
    if des_index == origin_index:
        net_reward += PENALTY["same_location"]

    # if +/- one hour from lunch time, reward system kicks in to reward agent
    # otherwise, penalise
    if df_destination.id in restaurant_indices:
        if curr_time >= LUNCH_TIME - 2 and curr_time <= LUNCH_TIME + 2:
            net_reward += REWARD["lunch"]
        else:
            net_reward += PENALTY["restaurant"]

    return net_reward


def plan_trip(planner):
    # unpack user input
    trip_days = planner.get_no_of_days()
    user_budget = planner.budget.id  # convert to numbers for comparison
    user_characterisations = planner.characterisation_scores

    q_table, no_of_destinations, attractions, restaurant_indices = initialisation()

    # train q model
    for i in range(1, iterations):

        cumulative_period = 0

        # default to start from first index in attractions list
        origin_index = 0

        # list of visisted destinations (in terms of indices and start from zero)
        destinations_visited = []

        for curr_time in range(0, PERIOD_PER_DAY):

            # decide on next step
            if random.uniform(0, 1) < EPSILON:
                destination_index = int(math.ceil(random.uniform(0, no_of_destinations - 1)))
            else:
                destination_index = int(np.argmax(q_table[origin_index, :, curr_time]))

            df_origin = attractions[origin_index]
            df_destination = attractions[destination_index]

            # calculate the reward for moving to the next destination
            reward = calculate_rewards(df_origin, df_destination, origin_index, destination_index, curr_time, restaurant_indices, user_characterisations, user_budget)

            # update q table with the q value for moving to next destination
            old_value = q_table[origin_index, destination_index, curr_time]
            next_max = np.max(q_table[destination_index, :, curr_time])
            new_value = (1 - ALPHA) * old_value + ALPHA * (reward + GAMMA * next_max)
            q_table[origin_index, destination_index, curr_time] = new_value

            # update state based on the next destination selection
            origin_index = destination_index
            destinations_visited.append(destination_index)

        if i % 5000 == 0:
            print("Current iteration : {}".format(i))

    # loop through numpy array hourly and print results
    for curr_time in range(0, PERIOD_PER_DAY):
        print("Current time: {} hr".format(curr_time))
        print(q_table[:, :, curr_time])

    for day in range(0, trip_days.days):

        origin_index = 0  # always start from origin
        destinations_per_day = [origin_index]
        df_origin = attractions[origin_index]
        cumulative_period = 0  # does not include time spent at origin

        if day == 0:
            destinations_visited = [origin_index]

        visit_time_left = 0
        restaurant_flag = False

        for curr_time in range(0, PERIOD_PER_DAY):
            # skip this step if still visiting a place
            if visit_time_left > 0:
                visit_time_left -= 1
                continue

            max_indices = np.argsort(q_table[origin_index, :, curr_time])[::-1]

            # once been to restaurant, we should not go there anymore
            if restaurant_flag:
                max_indices = [x for x in max_indices if x not in (destinations_visited + restaurant_indices)]
            else:
                max_indices = [x for x in max_indices if x not in destinations_visited]

            # run out of destinations to go then have to end there
            try:
                destination_index = int(max_indices[0])
            except IndexError:
                print("no more places to go")
                break

            df_destination = attractions[destination_index]

            cumulative_period += copy.copy(df_destination.period)
            visit_time_left = copy.copy(df_destination.period)

            destinations_visited.append(destination_index)
            destinations_per_day.append(destination_index)
            origin_index = destination_index

            if destination_index in restaurant_indices:
                restaurant_flag = True

        print("--- Day {} ---".format(day))
        print(cumulative_period)
        print(destinations_per_day)

        for attraction in [attractions[x] for x in destinations_per_day[1:]]:
            itinerary = Itinerary.objects.create(
                planner = planner,
                day = day + 1,
                attraction = attraction
            )
            e = itinerary.save()
            if e:
                raise e

