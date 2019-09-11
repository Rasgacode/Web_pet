import random


def creat_schedule(teams_out):
    schedule = {}
    for team in teams_out:
        for index, other_team in enumerate(teams_out):
            if index == 0:
                schedule[team['team_name']] = []
            if team['team_name'] != other_team['team_name']:
                schedule[team['team_name']].append(other_team['team_name'])
    return schedule


def creat_round(schedule):
    round_ = []
    random.shuffle(schedule)
    for match in schedule:
        if match['home'] not in round_ and match['away'] not in round_:
            round_ = round_ + [match['home'], match['away']]
    return [{'home': round_[index], 'away': round_[index + 1]} for index in range(0, len(round_), 2)]


def random_dices(team_rating):
    return [random.randint(1, 10) * (team_rating / 100) for times in range(5)]


def compare_dices(home_dices, away_dices):
    goals = {'home': 0, 'away': 0}
    for index in range(5):
        if home_dices[index] - 2 >= away_dices[index]:
            goals['home'] += 1
        elif away_dices[index] - 3 >= home_dices[index]:
            goals['away'] += 1
    return goals


def home_stats(home_team, goals):
    stat_to_upload = {'team_name': home_team}
