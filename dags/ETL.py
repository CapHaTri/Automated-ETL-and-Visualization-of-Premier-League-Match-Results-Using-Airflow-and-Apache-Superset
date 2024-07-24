from datetime import datetime, timedelta
import csv
import sys
from airflow import DAG
import pandas as pd
from airflow.operators.python import PythonOperator
import pymysql
import psycopg2
import requests
from bs4 import BeautifulSoup
import time
import smtplib


def crawl_and_store():
    standings_url = "https://fbref.com/en/comps/9/Premier-League-Stats"
    data = requests.get(standings_url, timeout=30)
    if data.status_code != 200:
        print(f"Request failed with status code {data.status_code}")
        return
    
    soup = BeautifulSoup(data.text, 'lxml')
    
    standings_tables = soup.select('table.stats_table')

    standings_table = standings_tables[0]
    
    links = standings_table.find_all('a')
    links = [l.get("href") for l in links]
    links = [l for l in links if '/squads/' in l]

    team_urls = [f"https://fbref.com{l}" for l in links]
    all_matches = []

    for team_url in team_urls:
        team_data = []
        team_name = team_url.split("/")[-1].replace("-Stats", "").replace("-", " ")
        data = requests.get(team_url)
        team_data = pd.read_html(data.text, match="Scores & Fixtures")[0]
        team_data = team_data[team_data["Comp"] == "Premier League"]
        team_data["Team"] = team_name
        all_matches.append(team_data)
        time.sleep(5)

    match_df = pd.concat(all_matches)
    match_df.columns = [c.lower() for c in match_df.columns]

    # Replace NaN values with None
    match_df = match_df.where(pd.notnull(match_df), None)

    db_opts = {
        'user': 'root',
        'password': 'sql',
        'host': 'mysql-db',
        'database': 'my_database',
        'port': 3306
    }

    conn = pymysql.connect(**db_opts)
    cur = conn.cursor()
    
    cur.execute("DROP TABLE IF EXISTS matches")
    create_table_query = '''
    CREATE TABLE matches (
        date DATE,
        time TIME,
        comp VARCHAR(50),
        round VARCHAR(50),
        day VARCHAR(50),
        venue VARCHAR(50),
        result VARCHAR(10),
        gf INT,
        ga INT,
        opponent VARCHAR(50),
        xg FLOAT,
        xga FLOAT,
        poss FLOAT,
        attendance INT,
        captain VARCHAR(50),
        formation VARCHAR(50),
        referee VARCHAR(50),
        match_report TEXT,
        notes TEXT,
        team VARCHAR(50)
    )
    '''
    cur.execute(create_table_query)

    for index, row in match_df.iterrows():
        cur.execute(
            "INSERT INTO matches (date, time, comp, round, day, venue, result, gf, ga, opponent, xg, xga, poss, attendance, captain, formation, referee, match_report, notes, team) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            tuple(row)
        )

    conn.commit()
    cur.close()
    conn.close()
    
    return True

def extract():
    db_opts = {
        'user': 'root',
        'password': 'sql',
        'host': 'mysql-db',
        'database': 'my_database',
        'port': 3306
    }

    db = pymysql.connect(**db_opts)
    cur = db.cursor()

    sql = 'SELECT * from matches'
    csv_file_path = 'matches_data.csv'

    try:
        cur.execute(sql)
        rows = cur.fetchall()
    finally:
        db.close()

    if rows:
        result = list()
        column_names = list()
        for i in cur.description:
            column_names.append(i[0])

        result.append(column_names)
        for row in rows:
            result.append(row)

        with open(csv_file_path, 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for row in result:
                csvwriter.writerow(row)
    else:
        sys.exit("No rows found for query: {}".format(sql))

    return True

def transform():
    # Đọc file CSV gốc
    df = pd.read_csv('matches_data.csv')

    # Khởi tạo bảng xếp hạng
    ranking = df.groupby('team').agg(
        matches=('team', 'count'),
        wins=('result', lambda x: (x == 'W').sum()),
        losses=('result', lambda x: (x == 'L').sum()),
        draws=('result', lambda x: (x == 'D').sum()),
        goals_for=('gf', 'sum'),
        goals_against=('ga', 'sum'),
        xg_avg=('xg', 'mean')
    ).reset_index()

    # Tính toán các cột bổ sung
    ranking['goal_difference'] = ranking['goals_for'] - ranking['goals_against']
    ranking['points'] = ranking['wins'] * 3 + ranking['draws'] * 1

    # Sắp xếp bảng xếp hạng theo điểm, hiệu số và số bàn thắng
    ranking = ranking.sort_values(by=['points', 'goal_difference', 'goals_for'], ascending=False)

    # Thêm cột vị trí trên bảng xếp hạng
    ranking['position'] = range(1, len(ranking) + 1)

    # Đổi tên các cột cho dễ đọc
    ranking.columns = ['Team', 'Matches', 'Wins', 'Losses', 'Draws', 'Goals For', 'Goals Against',
                       'xG_Avg', 'Goal Difference', 'Points', 'Position']

    # Lưu bảng xếp hạng vào file CSV mới
    ranking.to_csv('premier_league_ranking.csv', index=False)

    print("Bảng xếp hạng đã được lưu vào file 'premier_league_ranking.csv'.")
    return True

def load_to_postgres():
    conn = psycopg2.connect(
        dbname='postgres',
        user='postgres',
        password='postgres',
        host='postgresql-container',
        port=5432
    )
    cur = conn.cursor()

    out_csv_file_path = 'premier_league_ranking.csv'
    df = pd.read_csv(out_csv_file_path)

    cur.execute("DROP TABLE IF EXISTS premier_league_ranking")
    create_table_query = '''
    CREATE TABLE premier_league_ranking (
        Team VARCHAR(50),
        Matches INT,
        Wins INT,
        Losses INT,
        Draws INT,
        Goals_For INT,
        Goals_Against INT,
        xG_Avg FLOAT,
        Goal_Difference INT,
        Points INT,
        Position INT
    )
    '''
    cur.execute(create_table_query)

    for index, row in df.iterrows():
        cur.execute(
            "INSERT INTO premier_league_ranking (Team, Matches, Wins, Losses, Draws, Goals_For, Goals_Against, xG_Avg, Goal_Difference, Points, Position) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (row['Team'], row['Matches'], row['Wins'], row['Losses'], row['Draws'], row['Goals For'], row['Goals Against'], row['xG_Avg'], row['Goal Difference'], row['Points'], row['Position'])
        )

    conn.commit()
    cur.close()
    conn.close()

    return True

def send_email():
    # Thiết lập thông tin email
    email = 'captri03@gmail.com'
    receiver_email = 'trihx2003@gmail.com'
    subject = 'Updating : Premier League Ranking '
    
    # Đọc bảng xếp hạng từ file CSV
    ranking_file_path = 'premier_league_ranking.csv'
    df_ranking = pd.read_csv(ranking_file_path)
    
    # Tạo nội dung email
    ranking_summary = df_ranking.to_html(index=False)
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    message = f"""
    <html>
        <body>
            <h1>Premier League Ranking</h1>
            <p>ETL job completed at: {current_time}</p>
            <p>Here is the updating ranking:</p>
            {ranking_summary}
            <p>Thank you!</p>
        </body>
    </html>
    """
    
    # Thiết lập kết nối SMTP
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(email, "xakowcnepmwyiriz")
    
    # Tạo email
    msg = f"Subject: {subject}\nContent-Type: text/html\n\n{message}"
    
    # Gửi email
    server.sendmail(email, receiver_email, msg)
    
    # Đóng kết nối
    server.quit()

    return True

dag = DAG(
    'ETL_task',
    default_args={
        'email': ['trihx2003@gmail.com'],
        'email_on_failure': True,
        'retries': 1,
        'retry_delay': timedelta(minutes=5),
    },
    description='ETL DAG',
    schedule_interval="@once",
    start_date=datetime(2021, 6, 1),
    tags=['Capp']
)

crawl_operator = PythonOperator(
    task_id='crawl_data',
    python_callable=crawl_and_store,
    dag=dag
)

extract_operator = PythonOperator(
    task_id='load_from_mysql',
    python_callable=extract,
    dag=dag
)

transform_operator = PythonOperator(
    task_id='transform_data',
    python_callable=transform,
    dag=dag
)

load_to_postgres_operator = PythonOperator(
    task_id='load_to_postgres',
    python_callable=load_to_postgres,
    dag=dag
)

send_email_operator = PythonOperator(
    task_id='send_email',
    python_callable=send_email,
    dag=dag
)
crawl_operator >> extract_operator >> transform_operator >> load_to_postgres_operator >> send_email_operator
