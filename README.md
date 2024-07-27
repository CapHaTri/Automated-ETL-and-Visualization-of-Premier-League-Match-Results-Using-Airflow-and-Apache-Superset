# Automated ETL and Visualization of Premier League Match Results Using Airflow and Apache Superset

<img src="https://upload.wikimedia.org/wikipedia/en/thumb/f/f2/Premier_League_Logo.svg/800px-Premier_League_Logo.svg.png" alt="Premier League" width="300"/>

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Setup Instructions](#setup-instructions)
- [Data Pipeline](#data-pipeline)
- [Visualizations](#visualizations)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Introduction

This project aims to automate the process of extracting, transforming, and loading (ETL) Premier League match results, storing them in a PostgreSQL database, and visualizing the data using Apache Superset. The entire ETL workflow is managed by Apache Airflow, ensuring a scalable and reliable data pipeline.
## Features

- **Automated ETL Pipeline**: Using Apache Airflow to automate the process of extracting match data from an external API, transforming it into a usable format, and loading it into a PostgreSQL database.
- **Data Visualization**: Leveraging Apache Superset to create interactive dashboards and visualizations for analyzing Premier League match results.
- **Docker Compose Setup**: The project uses Docker Compose to streamline the deployment and management of the required services, including Apache Airflow, PostgreSQL, Redis, MySQL, and Apache Superset.
## Technologies Used

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
docker-compose up -d
cd Apache_Superset/
```
## Data Pipeline

- **Extraction**: Airflow DAG fetches match results data from an external API.
- **Transformation**: Data is cleaned and transformed into a format suitable for analysis.
- **Loading**: Transformed data is loaded into a PostgreSQL database for further analysis.
- **Scheduling**: Airflow schedules regular updates of the data pipeline.

## Visualizations

- **Dashboards**: Create interactive dashboards in Apache Superset to visualize match results, player statistics, and team performance.
- **Charts**: Use Superset's charting capabilities to generate graphs and tables that reflect the latest data.

## Usage

### Access Airflow

- Open [http://localhost:8080](http://localhost:8080) in your browser.
- Default credentials: `admin` / `admin`.

### Access Superset

- Open [http://localhost:8088](http://localhost:8088) in your browser.
- Default credentials: `admin` / `admin`.

### Trigger ETL Workflow

- In Airflow, manually trigger the ETL DAG or wait for the scheduled run.

### Explore Data

- In Superset, connect to the PostgreSQL database and use the available datasets to create charts and dashboards.

## Contributing

Contributions are welcome! Please fork the repository, make your changes, and submit a pull request. For bug reports or feature requests, open an issue in the GitHub repository.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For any questions or feedback, please reach out to [trihx2003@gmail.com](mailto:trihx2003@gmail.com).

   
