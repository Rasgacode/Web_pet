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
def creat_league_table_n_schedule(cursor, teams, schedule):
    cursor.execute("""
                    DROP TABLE IF EXISTS league_table;
                                       
                    CREATE TABLE league_table (
                    team_name character varying(255) NOT NULL,
                    played int DEFAULT 0,
                    won int DEFAULT 0,
                    drawn int DEFAULT 0,
                    lost int DEFAULT 0,
                    gf int DEFAULT 0,
                    ga int DEFAULT 0,
                    gd int DEFAULT 0,
                    points int DEFAULT 0
                    );
                    """)
    for item in teams:
        team = item['team_name']
        cursor.execute("""
                        INSERT INTO league_table
                        VALUES (%(team)s)
                        """, {'team': team})
    cursor.execute("""
                        DROP TABLE IF EXISTS schedule;
                        
                        CREATE TABLE schedule (
                        home character varying(255) NOT NULL,
                        away character varying(255) NOT NULL,
                        played character varying(255) NOT NULL DEFAULT 'no',
                        home_goals int DEFAULT NULL,
                        away_goals int DEFAULT NULL,
                        scorers character varying(255) DEFAULT NULL,
                        last character varying(255) DEFAULT 'notlast'
                        );
                        """)
    for home, aways in schedule.items():
        for team in aways:
            cursor.execute("""
                            INSERT INTO schedule
                            VALUES (%(home)s, %(team)s);
                            """, {'home': home,
                                  'team': team})


@database_common.connection_handler
def get_league_table(cursor):
    cursor.execute("""
                    SELECT * FROM league_table
                    """)
    return cursor.fetchall()


@database_common.connection_handler
def get_schedule(cursor):
    cursor.execute("""
                    SELECT home, away FROM schedule
                    WHERE played = 'no'
                    """)
    return cursor.fetchall()


@database_common.connection_handler
def set_played(cursor, last_round):
    for team in last_round:
        home_team = team['home']
        away_team = team['away']
        cursor.execute("""
                        UPDATE schedule
                        SET played = 'yes'
                        WHERE home = %(home_team)s and away = %(away_team)s
                        """, {'home_team': home_team,
                              'away_team': away_team})


@database_common.connection_handler
def set_last_round(cursor, next_round):
    cursor.execute("""
                    UPDATE schedule
                    SET last = 'notlast'
                    WHERE last = 'last'
                    """)
    for team in next_round:
        home_team = team['home']
        away_team = team['away']
        cursor.execute("""
                        UPDATE schedule
                        SET last = 'last'
                        WHERE home = %(home_team)s and away = %(away_team)s
                        """, {'home_team': home_team, 'away_team': away_team})


@database_common.connection_handler
def get_last_round(cursor):
    cursor.execute("""
                    SELECT home, away, home_goals, away_goals FROM schedule
                    WHERE last = 'last';
                    """)
    return cursor.fetchall()
