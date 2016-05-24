def big_six(answers):
    partial_score = 0

    # Assemble data structures
    veggie_servings = int(answers[1])
    fruit_servings = int(answers[2])
    checkbox_answers = {'read your scriptures today?': False,
                        'say your morning and evening prayers today?': False,
                        'go to sleep 7-8 hours before you woke up today?': False,
                        'drink at least 4 glasses of water today?': False}

    for pair in checkbox_answers.iteritems():
        if pair[0] in answers[0]:
            checkbox_answers[pair[0]] = True

    truth = [pair[1] for pair in checkbox_answers.iteritems()]

    # Add one point for each correct answer
    for item in truth:
        if item:
            partial_score += 1

    truth.append(veggie_servings)
    truth.append(fruit_servings)

    if all(item for item in truth):
        partial_score += 5

    partial_score += (veggie_servings + fruit_servings)
    return partial_score


def single_points(answers):
    partial_score = 0
    checkbox_answers = {"read or listen to at least 1 conference talk today?": False,
                        "document your life in some way? (journal writing, Savannah's jar, Kara's shutterfly, or some other kind of writing)": False,
                        "do at least 15 minutes of family history?": False}

    for pair in checkbox_answers.iteritems():
        if pair[0] in answers:
            checkbox_answers[pair[0]] = True
            partial_score += 1

    return partial_score


def bonus_points(answers):
    partial_score = 0
    checkbox_answers = {"deliberately get 15+ minutes of exercise?": False,
                        "go to the temple today?": False}

    for pair in checkbox_answers.iteritems():
        if pair[0] in answers:
            checkbox_answers[pair[0]] = True
            partial_score += 5

    return partial_score


def accountability(answers):
    partial_score = 0
    if answers[0] == 'Yes':
        partial_score -= 2
    else:
        partial_score += 2

    if answers[1] == 'Yes':
        partial_score -= 2
    else:
        partial_score += 2
    return partial_score
