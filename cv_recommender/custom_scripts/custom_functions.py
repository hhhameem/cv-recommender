import operator
import itertools


# function for categories as keys and no of time each category occurred as values
def jobs_in_dict_with_occurrence_number(all_jobs):
    category_dict = {}
    for job in all_jobs:
        category_dict[job.job_category] = category_dict\
            .get(job.job_category, 0)+1

    return category_dict


# function for sorting and slicing categories
def sort_dict_and_return(all_jobs):
    jobs_dict = jobs_in_dict_with_occurrence_number(all_jobs)
    sorted_cat_dict = dict(sorted(jobs_dict.items(),
                                  key=operator.itemgetter(1),
                                  reverse=True))

    sliced_dict = dict(itertools.islice(sorted_cat_dict.items(), 4))
    top_3 = dict(itertools.islice(sorted_cat_dict.items(), 3))

    return sorted_cat_dict, sliced_dict, top_3


# function for converting the strings into list and removing unwanted spaces
def convert_to_list(data_to_convert):
    list_to_return = []
    if data_to_convert == None:
        return 'None'
    else:
        remove_space_and_join = ' '.join(data_to_convert.split())
        splitted_data = remove_space_and_join.split(',')
        for item in splitted_data:
            list_to_return.append(item.strip().lower())
        return list_to_return
