# Recommendation engine for Etsy
#
# Calculates the Pearson Correlation between an application user and others
# who have favorited the same items. Uses this information to present the
# user with several potential items of interest.
#
# Author: Keyan Pishdadian 1/18/2015

from math import *
import requests
import api_key


def pearson_correlation(user_dict, user, other):
    """
    Returns the Pearson Correlation between two users.

    Takes a dictionary containing the items favorited by user 1
    and finds matching items favorited by user 2. Where user 1 is the
    application user. The Pearson score is calculated and returned.
    A score of 1 means that user 2 favorited every item that user 1 did,
    a score of 0 indicates no correlation. A score of < 0 is not possible
    in this model.
    """
    mutual_items = {}
    for item in user_dict[user]:
        if item in user_dict[other]:
            mutual_items[item] = 1

    # Number of items which are in both user's lists.
    matching_items = len(mutual_items)
    if matching_items == 0:
        return 0

    print other, mutual_items

    # Do some calculations now to reduce complexity of Pearson calculation
    user_sum = sum([user_dict[user][item] for item in mutual_items])
    other_sum = sum([user_dict[other][item] for item in mutual_items])

    sum_square_user = sum([pow(user_dict[user][item], 2)
    for item in mutual_items])
    sum_square_other = sum([pow(user_dict[other][item], 2)
    for item in mutual_items])

    product_sum = sum([user_dict[user][item] *
                       user_dict[other][item] for item in mutual_items])

    # print product_sum, sum_square_user, sum_square_other, user_sum, other_sum

    # Calulate Pearson score
    numerator = product_sum - (user_sum * other_sum / matching_items)
    denominator = sqrt((sum_square_user - pow(user_sum, 2) / matching_items) *
                       (sum_square_other - pow(other_sum, 2) / matching_items))

    if denominator == 0:
        return 0
    else:
        pearson_score = numerator/denominator
        return pearson_score


def top_user_matches(user_dict, application_user, n=10):
    """
    Returns a list of ten users with the highest similarity to the user.

    A wrapper for pearson_correlation(). Takes the list of items favorited by
    the application user and finds the Pearson score between the application
    user and others who have mutual favorited items.
    """
    matches = [(pearson_correlation(user_dict, application_user, other_user),
    other_user) for other_user in user_dict if other_user != application_user]

    matches.sort()
    matches.reverse()
    return matches[0:n]


def find_listing_favorites(listing_id):
    """
    Returns a list of users who have favorited the passed listing.

    Takes an Etsy listing_id and makes a findAllListingFavoredBy
    request to get back a set of FavoriteListing objects.
    """
    # In Etsy API as findAllListingFavoredBy
    r = requests.get('https://openapi.etsy.com/v2/listings/:listing_id/\
        favored-by?api_key={{api_key}}'.format(api_key=api_key.get_api_key()))

    if r == '403':
        return None


def find_user_favorite_list(used_id):
    """Returns a list of all listing_ids favorited by the user."""
    # In Etsy API as findAllUserFavoriteListings
    r = requests.get('https://openapi.etsy.com/v2/users/:user_id/favorites/\
        listings?api_key={{api_key}}'.format(api_key=api_key.get_api_key()))

    if r == '403':
        return None


def find_user_id(user_name):
    """
    Returns an int which is the numerical user_id for the user_name input.

    Takes a string which is the Etsy user_name and returns the int user_id,
    but only if the user has a public account. The user_id for private users
    cannot be accessed.
    """
    r = requests.get("https://openapi.etsy.com/v2/users/\
        :kpish?api_key={{api_key}}".format(api_key=api_key.get_api_key()))

    if r == '403':
        return None


if __name__ == "__main__":
    # r = requests.get("https://openapi.etsy.com/v2/users/\
    #     :kpish?api_key={{api_key}}".format(api_key=api_key.get_api_key()))

    # print r

    # print "https://openapi.etsy.com/v2/users/\
    # :kpish?api_key={{api_key}}".format(api_key=api_key.get_api_key())


    print top_user_matches(sample_data, 'keyan', 3)


