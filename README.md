# Automated ETL and Visualization of Premier League Match Results Using Airflow and Apache Superset

<img src="https://upload.wikimedia.org/wikipedia/en/thumb/f/f2/Premier_League_Logo.svg/800px-Premier_League_Logo.svg.png" alt="Premier League" width="300"/>

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Setup Instructions](#setup-instructions)
- [Data Pipeline](#data-pipeline)
- [Usage](#usage)
- [Visualizations](#visualizations)
- [Conclusion](#concly)
- [Future Direction](#Future_Direction)

## Introduction

This project aims to automate the process of extracting, transforming, and loading (ETL) Premier League match results, storing them in a PostgreSQL database, and visualizing the data using Apache Superset. The entire ETL workflow is managed by Apache Airflow, ensuring a scalable and reliable data pipeline.
## Features
- **Web Srapy:** Using BeautifulSoup to get data from EPL source, store in MySQL as datalake
- **Automated ETL Pipeline**: Using Apache Airflow to automate the process of collecting data into MySQL, extracting it from MySQL, transforming into a usable format, and loading into a PostgreSQL database. After that, using Smtplib to email about results
- **Data Visualization**: Leveraging Apache Superset to create interactive dashboards and visualizations for analyzing Premier League match results.
- **Docker Compose Setup**: The project uses Docker Compose to streamline the deployment and management of the required services, including Apache Airflow, PostgreSQL, Redis, MySQL, and Apache Superset.
## Technologies Used
- **BeautifulSoup** : For web scrapy
- **Apache Airflow**: For managing and scheduling ETL workflows.
- **PostgreSQL**: To store transformed match results data.
- **Redis**: Provides caching to enhance performance.
- **MySQL**: Optional, used for additional data storage.
- **Apache Superset**: For creating and managing data visualizations.
- **Docker Compose**: To orchestrate the deployment of the above technologies.

## Setup Instructions

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/Automated-ETL-and-Visualization-of-Premier-League-Match-Results-Using-Airflow-and-Apache-Superset.git
   cd Automated-ETL-and-Visualization-of-Premier-League-Match-Results-Using-Airflow-and-Apache-Superset
2. **Configuration**

- **Airflow Configuration**

  - Edit the file `airflow/dags/ETL.py` to configure your ETL tasks.

- **Superset Configuration**

  - Configure the connection to your PostgreSQL database in the Superset web interface after deployment.

- **Docker Compose Configuration**

  - Modify `docker-compose.yml` if necessary to suit your environment.

3.  **Start the Environment**

```bash
docker compose up -d
cd superset
docker compose -f docker-compose-image-tag.yml up #to run Apache Superset
```
## Data Pipeline
![image](https://github.com/user-attachments/assets/e8c3f81f-42ad-4fdd-a741-f2faedec1217)

- **Scrapy**: Collects data from the English Premier League (EPL) on fbref.com using BeautifulSoup and stores it in a MySQL database as Data lake.
- **Extraction**: Airflow DAG fetches match results data from MySQL Database.
- **Transformation**: Data is cleaned and transformed into a format suitable for analysis.
- **Loading**: Transformed data is loaded into a PostgreSQL database as Data WareHouse for further analysis.
- **Scheduling**: Airflow schedules regular updates of the data pipeline.
- **Email**: Sends an email notification upon completion of the ETL process, including updated results.
- **Analysis**: Analyzes the EPL data up to the current matches, providing detailed information about each team.

## Usage
### Raw Data

![image](https://github.com/user-attachments/assets/5928ce37-9df5-4b59-8356-7c67e15566ff)

### Access Airflow and Run ETL task

- Open [http://localhost:8080](http://localhost:8080) in your browser.
- Default credentials: `admin` / `admin`.
- Run ETL_Task
  
![image](https://github.com/user-attachments/assets/97fd0fa4-e99e-49ac-a6ef-4edfb997226a)

- After ETL_Task is done, receive email about ETL process and EPL information
  
  ![image](https://github.com/user-attachments/assets/fbbba438-9eba-423c-aa25-2d818a61db1a)

### Access Superset

- Open [http://localhost:8088](http://localhost:8088) in your browser.
- Default credentials: `admin` / `admin`.

### Explore Data

- In Superset, connect to the PostgreSQL database and use the available datasets to create charts and dashboards.
  
![image](https://github.com/user-attachments/assets/1478b49a-d2ec-4445-a496-ef5892d802f0)

## Visualizations

- Updates league standings, match counts, goal distribution, positions for European competitions and relegation.
  
  ![image](https://github.com/user-attachments/assets/0f449b1b-fa24-481b-94d2-fd3d143ac8db)

- Creates charts analyzing matches, goals, and other relevant metrics.
  
**Team: Manchester City**
![image](https://github.com/user-attachments/assets/4b6d9385-98b7-40b1-b0ce-6f6ae53a83b5)
**Team: Manchester United**
![image](https://github.com/user-attachments/assets/6f896586-2d09-4c41-87ea-b5c255d8a0bf)
**Team: Arsenal**
![image](https://github.com/user-attachments/assets/7c8829a3-2b2d-4a92-9327-605914219cdc)

## Conclusion
- The purpose of this project is to utilize ETL processes to continuously collect and update match results. This enables comprehensive analysis of the league and individual team performances, providing an up-to-date overview of the EPL as of the current matches.
## Future Direction
- We aim to gather additional data encompassing more detailed information. This will allow us to create more in-depth analytical charts and insights.
## Contact

For any questions or feedback, please reach out to [trihx2003@gmail.com](mailto:trihx2003@gmail.com).

   
