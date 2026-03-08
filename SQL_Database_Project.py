import sqlite3
import random
from datetime import datetime, timedelta

def generate_epl_synthetic_database():
    conn = sqlite3.connect('epl_synthetic_analytics.db')
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")

    cursor.executescript('''
        DROP TABLE IF EXISTS Match_Performances;
        DROP TABLE IF EXISTS Matches;
        DROP TABLE IF EXISTS Players;
        DROP TABLE IF EXISTS Teams;

        CREATE TABLE Teams (
            team_id INTEGER PRIMARY KEY AUTOINCREMENT,
            team_name TEXT NOT NULL,
            stadium TEXT NOT NULL
        );

        CREATE TABLE Players (
            player_id INTEGER PRIMARY KEY AUTOINCREMENT,
            team_id INTEGER,
            player_name TEXT NOT NULL,
            position TEXT NOT NULL,
            FOREIGN KEY (team_id) REFERENCES Teams (team_id)
        );

        CREATE TABLE Matches (
            match_id INTEGER PRIMARY KEY AUTOINCREMENT,
            home_team_id INTEGER,
            away_team_id INTEGER,
            match_date TEXT NOT NULL,
            temperature_celsius REAL,
            FOREIGN KEY (home_team_id) REFERENCES Teams (team_id),
            FOREIGN KEY (away_team_id) REFERENCES Teams (team_id)
        );

        CREATE TABLE Match_Performances (
            match_id INTEGER,
            player_id INTEGER,
            performance_rating TEXT,
            minutes_played INTEGER,
            distance_covered_km REAL,
            goals_scored INTEGER,
            PRIMARY KEY (match_id, player_id),
            FOREIGN KEY (match_id) REFERENCES Matches (match_id),
            FOREIGN KEY (player_id) REFERENCES Players (player_id)
        );
    ''')

    epl_teams = [
        ("Arsenal", "Emirates Stadium"), ("Aston Villa", "Villa Park"), ("Bournemouth", "Vitality Stadium"),
        ("Brentford", "Gtech Community Stadium"), ("Brighton", "Amex Stadium"), ("Chelsea", "Stamford Bridge"),
        ("Crystal Palace", "Selhurst Park"), ("Everton", "Goodison Park"), ("Fulham", "Craven Cottage"),
        ("Ipswich Town", "Portman Road"), ("Leicester City", "King Power Stadium"), ("Liverpool", "Anfield"),
        ("Manchester City", "Etihad Stadium"), ("Manchester United", "Old Trafford"), ("Newcastle United", "St James' Park"),
        ("Nottingham Forest", "City Ground"), ("Southampton", "St Mary's Stadium"), ("Tottenham", "Tottenham Hotspur Stadium"),
        ("West Ham", "London Stadium"), ("Wolves", "Molineux Stadium")
    ]
    cursor.executemany("INSERT INTO Teams (team_name, stadium) VALUES (?, ?)", epl_teams)

    # Synthetic Name Pools
    first_names = ["James", "Thomas", "Robert", "Edward", "William", "George", "Arthur", "Henry", "Oliver", "Harry", "Charlie", "Jack", "Noah", "Leo", "Jacob"]
    last_names = ["Smith", "Jones", "Taylor", "Brown", "Williams", "Wilson", "Johnson", "Davies", "Robinson", "Wright", "Thompson", "Evans", "Walker", "White", "Roberts"]

    positions = ["Goalkeeper", "Defender", "Midfielder", "Forward"]
    player_data = []
    for team_id in range(1, 21):
        for _ in range(20):
            # Mixing names randomly
            name = f"{random.choice(first_names)} {random.choice(last_names)}"
            pos = random.choices(positions, weights=[10, 35, 35, 20])[0]
            player_data.append((team_id, name, pos))

    cursor.executemany("INSERT INTO Players (team_id, player_name, position) VALUES (?, ?, ?)", player_data)

    # Generating 200 Matches
    start_date = datetime(2025, 8, 1)
    match_data = []
    for _ in range(200):
        t1, t2 = random.sample(range(1, 21), 2)
        m_date = start_date + timedelta(days=random.randint(0, 200))
        temp = round(random.uniform(-5.0, 25.0), 1)
        match_data.append((t1, t2, m_date.strftime('%Y-%m-%d'), temp))
    cursor.executemany("INSERT INTO Matches (home_team_id, away_team_id, match_date, temperature_celsius) VALUES (?, ?, ?, ?)", match_data)

    # Generating 4,400 Performance Records
    ratings = ["Poor", "Fair", "Good", "Excellent"]
    perf_data = []
    cursor.execute("SELECT match_id, home_team_id, away_team_id FROM Matches")
    for m_id, h_id, a_id in cursor.fetchall():
        cursor.execute("SELECT player_id, position FROM Players WHERE team_id IN (?, ?) LIMIT 22", (h_id, a_id))
        for p_id, pos in cursor.fetchall():
            dist = round(random.uniform(3.0, 13.0), 2)
            goals = random.choices([0, 1, 2], weights=[90, 8, 2])[0] if pos != "Goalkeeper" else 0
            perf_data.append((m_id, p_id, random.choice(ratings), random.randint(1, 90), dist, goals))

    cursor.executemany("INSERT INTO Match_Performances VALUES (?, ?, ?, ?, ?, ?)", perf_data)
    conn.commit()
    print(f"Synthetic database created with {len(perf_data)} records.")
    conn.close()

if __name__ == "__main__":
    generate_epl_synthetic_database()
