def form1_score(data):
    male = 0
    female = 0

    for ans in data.values():
        if ans == "yes":
            male += 1
        else:
            female += 1

    return "Male" if male >= female else "Female"


def form2_score(data):
    male = 0
    female = 0

    if data["h"] == "yes": male += 4
    else: female += 4

    if data["shoe"] == "yes": male += 3
    else: female += 3

    if data["beard"] == "yes": male += 9
    else: female += 5

    if data["voice"] == "yes": male += 1
    else: female += 1

    return "Male" if male >= female else "Female"
