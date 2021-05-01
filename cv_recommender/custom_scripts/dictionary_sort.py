import operator
import itertools


def sort_dict_and_return(category_dict):
    sorted_cat_dict = dict(sorted(category_dict.items(),
                                  key=operator.itemgetter(1),
                                  reverse=True))
    sliced_dict = dict(itertools.islice(sorted_cat_dict.items(), 8))
    top_3 = dict(itertools.islice(sorted_cat_dict.items(), 3))
    return sliced_dict, top_3
