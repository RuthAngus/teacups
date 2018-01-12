# An algorithm for finding groups of stars.

import numpy as np
import pandas as pd

# joint = pd.read_csv("joint.csv")
# star1 = joint.source_id1.values
# star2 = joint.source_id2.values

star1 = np.array([1, 2, 3, 4, 5, 6, 7, 9, 11, 13])
star2 = np.array([2, 1, 4, 5, 6, 7, 8, 10, 12, 8])
star_array = np.vstack((star1, star2)).T

mystar = 5
mygroup = []

def add_to_group_if_not_seen_before(masked_array, newgroup):
    print(masked_array)
    if len(masked_array):
        for st in masked_array:
            if not np.isin(st, newgroup):
                newgroup.append(st)
    return newgroup


def locate_star_and_add_to_group(star, star_array, group):
    newgroup = group*1
    m1 = star == star_array[:, 0]
    m2 = star == star_array[:, 1]
    newgroup = add_to_group_if_not_seen_before(star_array[:, 0][m1], newgroup)
    newgroup = add_to_group_if_not_seen_before(star_array[:, 1][m1], newgroup)
    newgroup = add_to_group_if_not_seen_before(star_array[:, 0][m2], newgroup)
    newgroup = add_to_group_if_not_seen_before(star_array[:, 1][m2], newgroup)
    return newgroup

# def find_star_iteration(star, star_array, mygroup):
#     new_group0 = locate_star_and_add_to_group(mystar, star_array, mygroup)
#     if len(new_group0) > len(mygroup):
#         print("stars added to newgroup")
#         mygroup = new_group0
#     else: print("no stars added")
#     print(mygroup)

def was_a_star_added(new_group0, mygroup):
    if len(new_group0) > len(mygroup):
        print("stars added to newgroup")
        mygroup = new_group0
    else: print("no stars added")
    print(mygroup)
    return mygroup

new_group0 = locate_star_and_add_to_group(mystar, star_array, mygroup)
mygroup = was_a_star_added(new_group0, mygroup)
new_group0 = locate_star_and_add_to_group(mygroup[0], star_array, mygroup)
mygroup = was_a_star_added(new_group0, mygroup)
new_group0 = locate_star_and_add_to_group(mygroup[0], star_array, mygroup)
mygroup = was_a_star_added(new_group0, mygroup)
new_group0 = locate_star_and_add_to_group(mygroup[1], star_array, mygroup)
mygroup = was_a_star_added(new_group0, mygroup)
new_group0 = locate_star_and_add_to_group(mygroup[2], star_array, mygroup)
mygroup = was_a_star_added(new_group0, mygroup)
new_group0 = locate_star_and_add_to_group(mygroup[3], star_array, mygroup)
mygroup = was_a_star_added(new_group0, mygroup)
