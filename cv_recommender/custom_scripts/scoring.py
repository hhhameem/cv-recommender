# check if job requires bonus skills.If requires then 50 marks is  distributed by
# 40 & 10 respectively on required and bonus.else, 50 is assigned only on required items
# returns 'per item score'
def score_per_skill(job):
    if job[1] != None:  # check if job requires bonus_skills
        per_required_item_score = 40.0/len(job[0])
        per_bonus_item_score = 10.0/len(job[1])
    else:
        per_required_item_score = 50.0/len(job[0])
        per_bonus_item_score = 0.0
    return per_required_item_score, per_bonus_item_score


# check if bonus_item_score is greater or smaller than 0. if <= 0 that means only required items
 # needs to be scoring and else both required and bonus needs to be scored
 # returns 'total score on skills'
def score_on_skills(job, application):
    per_required_item_score, per_bonus_item_score = score_per_skill(job)
    if per_bonus_item_score <= 0:  # that means no bonus skills are expected
        # comapre two list and returns common element
        common_required_skills = list(set(job[0]) & set(application[0]))
        total_score_on_skills = ((len(common_required_skills) * per_required_item_score) +
                                 per_bonus_item_score)   # multiply length of new list with per item score
    else:
        common_required_skills = list(set(job[0]) & set(application[0]))
        common_bonus_skills = list(set(job[1]) & set(application[1]))
        total_score_on_skills = ((len(common_required_skills)*per_required_item_score) +
                                 (len(common_bonus_skills)*per_bonus_item_score))   # multiply length of new list with per item score
    return total_score_on_skills


# if applicant_experience is greater than required experience then returns full score(30)
#  else, finds out the shortage experience and then assign scores on it
def score_on_experience(job, application):
    score_on_experience = 0
    experience_required = job[4]
    applicant_relevant_experience = application[4]
    experience = applicant_relevant_experience - experience_required
    if experience >= 0:
        score_on_experience = 30
    else:
        shortage_experience = (abs(experience)/experience_required)
        marks_for_shortage_experience = shortage_experience*30
        score_on_experience = 30 - marks_for_shortage_experience
    return score_on_experience


# if applicant level of education is similar or higher than required,15 marks are assigned.else,10 marks.
# return the score on level_of_education which is either 15 or 10
def level_of_education(level_of_education_required, applicant_education_level):
    education_level_score = 0
    if (level_of_education_required == 'post graduate'):
        if (applicant_education_level == 'post graduate'):
            education_level_score = 15
        else:
            education_level_score = 10
    elif (level_of_education_required == 'graduate'):
        if (applicant_education_level == 'graduate'):
            education_level_score = 15
        elif (applicant_education_level == 'post graduate'):
            education_level_score = 15
        else:
            education_level_score = 10
    elif (level_of_education_required == 'hsc'):
        if (applicant_education_level == 'hsc'):
            education_level_score = 15
        elif (applicant_education_level == 'graduate'):
            education_level_score = 15
        elif (applicant_education_level == 'post graduate'):
            education_level_score = 15
        else:
            education_level_score = 10
    elif (level_of_education_required == 'ssc'):
        education_level_score = 15
    return education_level_score


# if level of education is ssc or hsc marks are comapared with gpa 5.00.else, gpa 4.00 and highest marks 5.
# return the score on cgpa which is 5 or less
def cgpa(cgpa_required, applicant_cgpa, level_of_education_required):
    cgpa_score = 0
    if level_of_education_required == 'ssc' or 'hsc':
        if cgpa_required > applicant_cgpa:        # equation same as experience
            shortage_cgpa = ((cgpa_required-applicant_cgpa)/cgpa_required)
            marks_for_shortage_cgpa = shortage_cgpa*5.00
            cgpa_score = 5.00 - marks_for_shortage_cgpa
        else:
            cgpa_score = 5.00
    else:
        if cgpa_required > applicant_cgpa:
            shortage_cgpa = ((cgpa_required-applicant_cgpa)/cgpa_required)
            marks_for_shortage_cgpa = shortage_cgpa*4.00
            cgpa_score_to_be_converted = 4.00 - marks_for_shortage_cgpa
            # converting marks of cgpa 4 into 5
            cgpa_score = ((cgpa_score_to_be_converted/4.00)*5)
        else:
            cgpa_score = 5.00
    return cgpa_score


# return total score on education
def score_on_education(job, application):
    level_of_education_required = job[2][0]
    cgpa_required = job[3]
    applicant_education_level = application[2][0]
    applicant_cgpa = application[3]
    score_on_level_of_education = level_of_education(
        level_of_education_required, applicant_education_level)
    score_on_cgpa = cgpa(cgpa_required, applicant_cgpa,
                         level_of_education_required)
    total_score_on_education = (score_on_level_of_education + score_on_cgpa)
    return total_score_on_education


# the MOTHER function
#  returns total score
def score_of_an_applicant(job, application):
    skill = score_on_skills(job, application)
    experience = score_on_experience(job, application)
    education = score_on_education(job, application)
    return skill+experience+education
