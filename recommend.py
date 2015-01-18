# Recommendation engine
#
# Author: Keyan Pishdadian 1/18/2015


def pearson_correlation(items_dict, user1, user2):
    """
    Takes the Pearson Correlation between two users.

    Takes a dictionary containing the items favorited/liked by user 1
    and finds matching items favorited by user 2. The Pearson score is
    calculated and returned. Where a score of 1 means that user 2
    favorited every item that user 1 did, a score of 0 indicates no
    correlation, and a score of -1 indicates a negative correlation.
    """
    mutual_items = {}
    for item in items_dict[user1]:
        if item in items_dict[user2]:
            mutual_items[item] = 1

    # Number of items which are in both user's lists.
    matching_items = len(mutual_items)
    if matching_items == 0:
        return 0

    sum1 = sum([items_dict[user1][item] for item in mutual_items])
    sum2 = sum([items_dict[user2][item] for item in mutual_items])

    sum_squares_1 = sum([items_dict[user1][items] for item in matching_items])
    sum_squares_2 = sum([items_dict[user1][items] for item in matching_items])

    product_sum = sum
    
