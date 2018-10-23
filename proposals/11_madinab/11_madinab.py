import csv
import matplotlib
import json
from flask import Flask, request, render_template
app = Flask(__name__)


def get_races_list():
    with open('Somerville_High_School_YRBS_Raw_Data_2002-2016.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = -1
        races = set()
        races_index = 0
        for row in csv_reader:
            if line_count == -1:
                for index, quality in enumerate(row):
                    if quality == 'race':
                        races_index = index
                    line_count += 1
            else:
                type_of_race = row[races_index]
                if type_of_race not in races:
                    races.add(type_of_race)
        races = sorted(races, key=len, reverse=True)
        return races


def get_genders_list():
    with open('Somerville_High_School_YRBS_Raw_Data_2002-2016.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = -1
        genders = set()
        genders_index = 0
        for row in csv_reader:
            if line_count == -1:
                for index, quality in enumerate(row):
                    if quality == 'gender':
                        genders_index = index
                    line_count += 1
            else:
                type_of_gender = row[genders_index]
                if type_of_gender not in genders:
                    genders.add(type_of_gender)
        genders = sorted(genders, key=len, reverse=True)
        return genders


def show_genders_text(genders):
    for gender in genders:
        for type_of_friends in genders[gender]:
            print 'There are ', genders[gender][type_of_friends], ' ', gender, ' people who have ', type_of_friends, ' friends.'


def show_races_text(races):
    for race in races:
        for type_of_friends in races[race]:
            print 'There are ', races[race][type_of_friends], ' ', race, ' people who have ', type_of_friends, ' friends.'


def get_types_of_friendship():
    with open('Somerville_High_School_YRBS_Raw_Data_2002-2016.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = -1
        friends = []
        friends_index = 0
        for row in csv_reader:
            if line_count == -1:
                for index, quality in enumerate(row):
                    if quality == 'friends':
                        friends_index = index
                        line_count += 1
            else:
                type_of_friends = row[friends_index]
                if type_of_friends not in friends:
                    friends.append(type_of_friends)
    return friends


def get_friends_total():
    with open('Somerville_High_School_YRBS_Raw_Data_2002-2016.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = -1
        friends = {}
        genders_index = 0
        races_index = 0
        friends_index = 0
        for row in csv_reader:
            if line_count == -1:
                for index, quality in enumerate(row):
                    if quality == 'race':
                        races_index = index
                    if quality == 'gender':
                        genders_index = index
                    if quality == 'friends':
                        friends_index = index
                    line_count += 1
            else:
                type_of_race = row[races_index]
                type_of_gender = row[genders_index]
                has_friends = row[friends_index]
                if type_of_race not in friends:
                    friends[type_of_race] = {}
                if type_of_gender not in friends[type_of_race]:
                    friends[type_of_race][type_of_gender] = {}
                if has_friends not in friends[type_of_race][type_of_gender]:
                    friends[type_of_race][type_of_gender][has_friends] = 0
                    #print type_of_race, has_friends, type_of_gender
                friends[type_of_race][type_of_gender][has_friends] += 1
        return friends


@app.route('/')
def main():
    return render_template(
        "index.html",
        types_of_friendship=types_of_friendship,
        genders=genders,
        races=races,
        friends=friends,
        groups=groups)


def get_groups(selected_races, selected_genders, selected_friendship):
    groups = []
    group = {}
    races_set = selected_races
    genders_set = selected_genders
    friendship_set = selected_friendship
    r = True
    g = True
    f = True

    if len(selected_races) == 0:
        r = False
        races_set = races
    if len(genders_set) == 0:
        g = False
        genders_set = genders
    if len(friendship_set) == 0:
        f = True
        friendship_set = types_of_friendship

    for race in races_set:
        if race in friends:
            for gender in genders_set:
                if gender in friends[race]:
                    for type_of_friendship in friendship_set:
                        if type_of_friendship in friends[race][gender]:
                            gender_str = gender
                            race_str = race
                            type_of_friendship_str = type_of_friendship
                            if type_of_friendship == ' ':
                                type_of_friendship_str = 'not defined'
                            if race == ' ':
                                race_str = 'not defined'
                            if gender == ' ':
                                gender_str = 'not defined'

                            key = ' '
                            if r:
                                key += race_str
                                key += ' '

                            if g:
                                key += gender_str
                                key += ' '
                            key += "people with "
                            if f:
                                key += type_of_friendship_str
                                key += ' '

                            key += "friends"

                            value = friends[race][gender][type_of_friendship]

                            if key not in group:
                                group[key] = 0
                            group[key] += value

    groups.append(group)
    return groups


@app.route('/show_chart', methods=['POST'])
def show_chart():
    selected_genders = request.form.getlist("genders")
    selected_races = request.form.getlist("races")
    selected_types_of_friendship = request.form.getlist("type_of_friendship")
    print selected_races, selected_types_of_friendship
    groups = get_groups(
        selected_races,
        selected_genders,
        selected_types_of_friendship)
    return render_template(
        "index.html",
        types_of_friendship=types_of_friendship,
        genders=genders,
        races=races,
        friends=friends,
        groups=groups)


if __name__ == '__main__':
    types_of_friendship = get_types_of_friendship()
    friends = get_friends_total()
    genders = get_genders_list()
    races = get_races_list()
    groups = get_groups([], [], [])
    app.secret_key = 'some_data'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
