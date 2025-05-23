import requests
from bs4 import BeautifulSoup
import pandas as pd
import mysql.connector
from mysql.connector import Error
import logging
from typing import Optional
import re

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("companies_etl.log"),
        logging.StreamHandler(),
    ],
)

class CompaniesETL:
    """Class to extract, transform, and load company data from Wikipedia to MySQL."""

    def __init__(self):
        self.url = "https://en.wikipedia.org/wiki/List_of_largest_companies_in_the_United_States_by_revenue"
        self.db_config = {
            "host": "localhost",
            "database": "companies_db",  # Database must exist
            "user": "*****",  # Replace with your MySQL user
            "password": "*****"  # Replace with your MySQL password
        }

    def _create_database(self):
        """Create the database if it doesn't exist."""
        try:
            conn = mysql.connector.connect(
                host=self.db_config["host"],
                user=self.db_config["user"],
                password=self.db_config["password"],
            )
            cursor = conn.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.db_config['database']}")
            conn.commit()
            cursor.close()
            conn.close()
            logging.info(f"Database {self.db_config['database']} created successfully.")
        except Error as e:
            logging.error(f"Error creating database: {e}")
            raise

    def _extract(self) -> Optional[pd.DataFrame]:
        """Extract data from Wikipedia."""
        try:
            logging.info(f"Extracting data from {self.url}")
            response = requests.get(self.url)
            response.raise_for_status()  # Check if the request was successful

            soup = BeautifulSoup(response.text, "html.parser")
            table = soup.find_all("table")[1]  # Select the second table

            # Extract headers
            headers = [th.text.strip() for th in table.find_all("th")]

            # Extract data
            data = []
            for row in table.find_all("tr")[1:]:  # Skip the header row
                cols = row.find_all("td")
                data.append([col.text.strip() for col in cols])

            df = pd.DataFrame(data, columns=headers)
            logging.info(f"{len(df)} companies extracted successfully.")
            return df

        except Exception as e:
            logging.error(f"Extraction failed: {e}")
            return None

    def _transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean and structure the data."""
        try:
            logging.info("Transforming data...")

            # Clean column names
            df.columns = [col.replace("\n", " ").replace(" (USD billions)", "").strip() for col in df.columns]

            # Rename columns
            df = df.rename(columns={
                "Revenue": "revenue_billions",
                "Headquarters": "hq_location",
            })

            # Convert revenue to float
            df["revenue_billions"] = df["revenue_billions"].apply(lambda x: float(re.sub(r"\[.*\]", "", x)))

            # Extract city and state from headquarters location
            df["hq_city"] = df["hq_location"].apply(lambda x: x.split(",")[0].strip() if "," in x else None)
            df["hq_state"] = df["hq_location"].apply(lambda x: x.split(",")[1].strip() if "," in x else None)

            # Convert employee count to integer
            df["Employees"] = df["Employees"].str.replace(",", "").astype(int)

            # Add simplified industry category
            df["industry_category"] = df["Industry"].apply(
                lambda x: "Retail" if "Retail" in x
                else "Food" if "Food" in x
                else "Energy" if "Petroleum" in x
                else "Other"
            )

            # Add timestamp
            df["extracted_at"] = pd.Timestamp.now()

            logging.info("Transformation completed successfully.")
            return df

        except Exception as e:
            logging.error(f"Transformation failed: {e}")
            raise

    def _create_db_connection(self):
        """Establish a MySQL connection."""
        try:
            conn = mysql.connector.connect(**self.db_config)
            return conn
        except Error as e:
            logging.error(f"Failed to connect to MySQL: {e}")
            raise

    def _init_db_table(self):
        """Create the table if it doesn't exist."""
        try:
            conn = self._create_db_connection()
            cursor = conn.cursor()

            create_table_query = """
            CREATE TABLE IF NOT EXISTS largest_companies (
                id INT AUTO_INCREMENT PRIMARY KEY,
                `rank` INT,
                name VARCHAR(255) NOT NULL,
                industry VARCHAR(255),
                revenue_billions DECIMAL(10,2),
                employees INT,
                hq_location VARCHAR(255),
                hq_city VARCHAR(255),
                hq_state VARCHAR(100),
                industry_category VARCHAR(100),
                extracted_at DATETIME,
                UNIQUE KEY unique_company (name, extracted_at)
            )
            """
            cursor.execute(create_table_query)
            conn.commit()
            cursor.close()
            conn.close()
            logging.info("MySQL table initialized successfully.")

        except Error as e:
            logging.error(f"Failed to create table: {e}")
            raise

    def _load_to_db(self, df: pd.DataFrame):
        """Load data into MySQL."""
        try:
            conn = self._create_db_connection()
            cursor = conn.cursor()

            # Prepare data for insertion
            records = []
            for _, row in df.iterrows():
                records.append((
                    int(row[0]),  # Rank
                    row["Name"],
                    row["Industry"],
                    float(row["revenue_billions"]),
                    int(row["Employees"]),
                    row["hq_location"],
                    row.get("hq_city"),
                    row.get("hq_state"),
                    row.get("industry_category"),
                    row["extracted_at"],
                ))

            # Insert query
            insert_query = """
            INSERT INTO largest_companies (
                `rank`, name, industry, revenue_billions, employees,
                hq_location, hq_city, hq_state, industry_category, extracted_at
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.executemany(insert_query, records)
            conn.commit()

            logging.info(f"{len(df)} companies loaded into MySQL.")
            cursor.close()
            conn.close()

        except Error as e:
            logging.error(f"Failed to load data into MySQL: {e}")
            raise

    def run_pipeline(self):
        """Run the complete ETL pipeline."""
        try:
            logging.info("Starting ETL pipeline...")

            # 1. Create the database if it doesn't exist
            self._create_database()

            # 2. Extract data
            raw_data = self._extract()
            if raw_data is None:
                raise ValueError("Extraction failed.")

            # 3. Transform data
            transformed_data = self._transform(raw_data)

            # 4. Initialize MySQL table
            self._init_db_table()

            # 5. Load data into MySQL
            self._load_to_db(transformed_data)

            logging.info("ETL pipeline completed successfully!")
            return transformed_data

        except Exception as e:
            logging.error(f"ETL pipeline failed: {e}")
            raise

if __name__ == "__main__":
    etl = CompaniesETL()
    result = etl.run_pipeline()
    print(result.head())  # Display the first 5 companies