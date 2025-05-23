# Companies ETL Pipeline

This project provides an ETL (Extract, Transform, Load) pipeline to scrape data about the largest U.S. companies by revenue from Wikipedia, transform it, and load it into a MySQL database.

## Prerequisites

- Python 3.8 or higher
- MySQL Server installed and running
- Git (optional, for cloning the repository)

## Installation

1. **Set Up a Virtual Environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install Required Libraries**:
   Install the necessary Python packages using pip:
   ```bash
   pip install requests beautifulsoup4 pandas mysql-connector-python
   ```
   The required libraries are:
   - `requests`: For making HTTP requests to fetch the Wikipedia page.
   - `beautifulsoup4`: For parsing HTML content.
   - `pandas`: For data manipulation and transformation.
   - `mysql-connector-python`: For connecting to and interacting with MySQL.

3. **Set Up MySQL**:
   - Ensure MySQL Server is installed and running.
   - Create a MySQL user with appropriate permissions or use an existing user (e.g., `root`).

## Configuration

1. **Update Database Credentials**:
   Open the `companies_etl.py` file and locate the `db_config` dictionary in the `CompaniesETL` class:
   ```python
   self.db_config = {
       "host": "localhost",
       "database": "companies_db",  # Database name
       "user": "****",  # Replace with your MySQL user
       "password": "*****",  # Replace with your MySQL password
   }
   ```
   - Replace `"companies_db"` with your desired database name.
   - Replace `"****"` with your MySQL username.
   - Replace `"*****"` with your MySQL password.

2. **Create the Database**:
   The script automatically creates the database if it doesn't exist. Ensure your MySQL user has permission to create databases. Alternatively, manually create the database:
   ```sql
   CREATE DATABASE companies_db;
   ```

## Running the ETL Pipeline

1. **Execute the Script**:
   From the project directory, run the ETL pipeline:
   ```bash
   python companies_etl.py
   ```
   The script will:
   - Extract data from the Wikipedia page: [List of largest companies in the United States by revenue](https://en.wikipedia.org/wiki/List_of_largest_companies_in_the_United_States_by_revenue).
   - Transform the data (clean column names, convert data types, add derived fields).
   - Load the data into the `largest_companies` table in the specified MySQL database.

2. **Verify Output**:
   - The script logs progress to both the console and a file named `companies_etl.log`.
   - The script prints the first five rows of the transformed data to the console.
   - Check the MySQL database to confirm the data has been loaded:
     ```sql
     USE companies_db;
     SELECT * FROM largest_companies LIMIT 5;
     ```

## Project Structure

- `companies_etl.py`: Main Python script containing the ETL pipeline logic.
- `companies_etl.log`: Log file generated during execution, containing pipeline status and errors.

## Logging

The pipeline uses Python's `logging` module to record events:
- Logs are saved to `companies_etl.log`.
- Logs are also displayed in the console for real-time monitoring.
- Log levels include `INFO` for progress and `ERROR` for issues.

## Notes

- Ensure a stable internet connection for data extraction from Wikipedia.
- If MySQL connection issues occur, verify the database server is running and credentials are correct.
- The script assumes the second table on the Wikipedia page contains the relevant data. If the page structure changes, the script may need updates.
- The `largest_companies` table includes a unique constraint on `name` and `extracted_at` to prevent duplicate entries.

## Troubleshooting

- **MySQL Connection Errors**:
  - Check that the MySQL server is running: `sudo service mysql status` (Linux) or equivalent.
  - Verify the username and password in `db_config`.
- **HTTP Request Errors**:
  - Ensure the Wikipedia URL is accessible and unchanged.
  - Check your internet connection.
- **Data Transformation Errors**:
  - Inspect the `companies_etl.log` file for detailed error messages.
  - Verify the Wikipedia page structure hasn't changed.

