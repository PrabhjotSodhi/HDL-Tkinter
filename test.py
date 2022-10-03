categories = {
    'a': [1,1,2,3,4],
    'b':[1,1,2,3,4,5,6],
    'c':[1,1,2],
    'd':[1,1,1,1,1,1,1,4]
}

categories2 = {
    'plan_to_watch': [129760, 157383, 157383, 157383, 157383, 157383, 157383, 157383, 157383, 157383, 93405, 93405, 93405, 93405, 93405, 93405, 93405, 93405, 93405, 93405],
    'currently_watching': [93405],
    'completed': [93405, 93405],
    'on_hold': [],
    'dropped': [93405]
}

for category in categories:
    for id in categories[category]:
        if id == 1:
            while 1 in categories[category]:
                categories[category].remove(id)
print(categories)

for category in categories2:
    for id in categories2[category]:
        if id == 93405:
            while 93405 in categories2[category]:
                categories2[category].remove(id)
print(categories2)