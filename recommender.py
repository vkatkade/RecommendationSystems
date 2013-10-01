# Copyright (c) 2013 Vaibhav Katkade (vkatkade@gmail.com)
# Description: This is an illustration of a Recommendation System based on Collaborative User-User Filtering. 
#              The system simply looks at movies voted on by users and does not take in to account the actual rating itself.
# Input: A MovieID
# Output: Top 5 movies which were voted by other users who also rated the MovieID entered in input. 

import sys
import csv
from collections import defaultdict
from collections import OrderedDict

movies_file = 'recsys-data-movie-titles.csv'
ratings_file = 'recsys-data-ratings.csv'

movie_titles = defaultdict(list) # Table for Mapping Movie-ID to Movie Titles
top_related_movies = [] # Output list of top 5 related movies


def movie_id_to_title(movieid):
    return movie_titles[movieid]

def parse_movie_titles():
    with open(movies_file) as f:
        reader = csv.DictReader(f)
        for row in reader:
            movie_titles[row['mid']].append(row['title'])

def compute_top_movies(mymovid):
    # Initialize the Dictionary of MovieID-UserID
    rdict = defaultdict(list)
    # Initialize the Dictionary of UserID-MovieID 
    fdict = defaultdict(list)

    # Populate the MovieID-UserID Dictionary and UserID-MovieID Dictionary
    with open(ratings_file) as f:
        reader = csv.DictReader(f)  # create a reader which represents rows in a dictionary form
        for row in reader:  # this will read a row as {column1: value1, column2: value2,...}
            rdict[row['mid']].append(row['uid'])
            fdict[row['uid']].append(row['mid'])


    # The list of UserIDs matching my MovieID (x)
    uids_for_my_movid = rdict[mymovid]

    # Number of users who also like my MovieID count(x)
    n_users_mymovieid = len(uids_for_my_movid)

    # Users who do NOT like my MovieID (!x)
    uids_not_my_movid = []
    for i_userid in fdict:
        if mymovid not in fdict[i_userid]:
            uids_not_my_movid.append(i_userid)

    # Number of users do NOT like my MovieID count(!x)
    n_users_not_mymovieid = len(uids_not_my_movid)

    scoring_ratio = {}

    # Now Iterate through the dictionary and find out counts of (x && y), and (!x && y) for every MovieID
    for i_movid in rdict:
      count_x_y = 0
      count_nx_y = 0
      for i_usid_for_mymov in uids_for_my_movid:
          if i_usid_for_mymov in rdict[i_movid]:
              count_x_y += 1
      for i_usid_not_mymov in uids_not_my_movid:
          if i_usid_not_mymov in rdict[i_movid]:
              count_nx_y += 1
      if count_nx_y == 0:
          count_nx_y = n_users_not_mymovieid
      scoring_ratio[i_movid] = float(count_x_y / float(n_users_mymovieid)) / float(count_nx_y / float(n_users_not_mymovieid))

    # Now Order the scoring ratio table by values to obtain the list of top MovieIDs and their respective similarity ratios
    smcounts = OrderedDict(sorted(scoring_ratio.items(), key=lambda x: x[1], reverse=True))
#    for i in range(6):
#       k = smcounts.keys()[i] 
#       print mymovid + "," + k + "," + str("%.2f" % smcounts[k])
    for i in range(6):
       k = smcounts.keys()[i]
       top_related_movies.append(k)


def print_syntax():
    print "Syntax: python recommender.py <movieid>"

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print_syntax()
        exit()
    mymovid = sys.argv[1]
    parse_movie_titles()
    print "Entered movie is: " + mymovid +" - " + movie_id_to_title(mymovid)[0]
    print "Computing related movies..."
    compute_top_movies(mymovid)
    print "Top 5 Related Movies are:"
    for mid in range(len(top_related_movies)):
        print top_related_movies[mid] + " - " + movie_id_to_title(top_related_movies[mid])[0]

