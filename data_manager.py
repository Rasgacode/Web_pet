import database_common


@database_common.connection_handler
def get_teams(cursor, position):
    cursor.execute("""
                    SELECT team_name, player_1, player_2, player_3 FROM football_table
                    WHERE position = %(position)s;
                    """, {'position': position})
    return cursor.fetchall()


@database_common.connection_handler
def update_position(cursor, team):
    cursor.execute("""
                    UPDATE football_table
                    SET position = 'out'
                    WHERE team_name = %(team)s
                    """, {'team': team})


@database_common.connection_handler
def set_pos_def(cursor):
    cursor.execute("""
                    UPDATE football_table
                    SET position = 'in'
                    WHERE position = 'out'
                    """)


@database_common.connection_handler
def creat_league_table_n_schedule(cursor, teams, schedule, user_id):
    cursor.execute("""
                        DELETE FROM league_table
                        WHERE user_id = %(user_id)s
                        """, {'user_id': user_id})
    for item in teams:
        team = item['team_name']
        cursor.execute("""
                        INSERT INTO league_table (user_id, team_name)
                        VALUES (%(user_id)s, %(team)s)
                        """, {'team': team, 'user_id': user_id})
        cursor.execute("""
                            DELETE FROM schedule
                            WHERE user_id = %(user_id)s
                            """, {'user_id': user_id})
    for home, aways in schedule.items():
        for team in aways:
            cursor.execute("""
                            INSERT INTO schedule (user_id, home, away)
                            VALUES (%(user_id)s, %(home)s, %(team)s);
                            """, {'home': home,
                                  'team': team,
                                  'user_id': user_id})


@database_common.connection_handler
def get_league_table(cursor, user_id):
    cursor.execute("""
                    SELECT team_name, played, won, drawn, lost, gf, ga, gd, points FROM league_table
                    WHERE user_id = %(user_id)s
                    """, {'user_id': user_id})
    return cursor.fetchall()


@database_common.connection_handler
def get_schedule(cursor, user_id):
    cursor.execute("""
                    SELECT home, away FROM schedule
                    WHERE played = 'no' AND user_id = %(user_id)s
                    """, {'user_id': user_id})
    return cursor.fetchall()


@database_common.connection_handler
def set_played(cursor, last_round, user_id):
    for team in last_round:
        home_team = team['home']
        away_team = team['away']
        cursor.execute("""
                        UPDATE schedule
                        SET played = 'yes'
                        WHERE home = %(home_team)s and away = %(away_team)s and user_id = %(user_id)s
                        """, {'home_team': home_team,
                              'away_team': away_team,
                              'user_id': user_id})


@database_common.connection_handler
def set_last_round(cursor, next_round, user_id):
    cursor.execute("""
                    UPDATE schedule
                    SET last = 'notlast'
                    WHERE last = 'last' and user_id = %(user_id)s
                    """, {'user_id': user_id})
    for team in next_round:
        home_team = team['home']
        away_team = team['away']
        cursor.execute("""
                        UPDATE schedule
                        SET last = 'last'
                        WHERE home = %(home_team)s and away = %(away_team)s and user_id = %(user_id)s
                        """, {'home_team': home_team,
                              'away_team': away_team,
                              'user_id': user_id})


@database_common.connection_handler
def get_last_round(cursor, user_id):
    cursor.execute("""
                    SELECT home, away, home_goals, away_goals FROM schedule
                    WHERE last = 'last' and user_id = %(user_id)s;
                    """, {'user_id': user_id})
    return cursor.fetchall()
