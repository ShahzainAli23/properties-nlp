# properties-nlp

This project is a Python-based application that interacts with OpenAI's GPT model to generate SQL queries based on user input. It then executes the generated SQL query against a MySQL database and displays the results. The application also uses environment variables for storing sensitive information like API keys and database credentials.

## Prerequisites

To run this project, you will need:

- Python 3.x
- A MySQL database

## Libraries Needed

To run this project, you'll need to install the following Python libraries:

- `streamlit` – For building the web app.
- `openai` – For interacting with the GPT model (used via Azure in this case).
- `mysql-connector-python` – To interact with the MySQL database.
- `python-dotenv` – For loading environment variables from a `.env` file.
- `pandas` – For working with the data and displaying it in tabular form.
- `os` – For accessing system-level environment variables.

## Installation

You can install all required libraries using `pip`:

```bash
pip install streamlit openai mysql-connector-python python-dotenv pandas

## Setup

### 1. Environment Variables

Edit the `.env` file in the root directory of the project and replace the dummy values with your actual credentials.

# Host address for the MySQL database connection (replace with actual host)
host = your_database_host_here

# Username for connecting to the MySQL database (replace with actual username)
user = your_database_user_here

# Password for the MySQL user (replace with actual password)
password = your_database_password_here

# Name of the database to use for queries (replace with actual database name)
database_name = your_database_name_here

# Name of the table in the database (keep the name as 'properties')
table_name = your_table_name_here
```

### 2. Database Setup

This project works with a MySQL database. To set up the database:

1. I have attached an `.sql` file that contains the schema for the database. 
2. The data for the database was created by converting the XML file into a CSV format, and then importing this CSV into MySQL. This step was essential to structure the data in a way that can be used effectively by the application. The attached `.sql` file contains the necessary queries for creating the required tables and importing the data into the database.

You can use the `.sql` file to set up your database schema and import the data.

### 3. Running the Application

Once the setup is complete, you can run the application:

```bash
streamlit run app.py
```

The program will prompt you to input a search query. Based on your input, it will generate an SQL query using OpenAI's GPT model, execute the query against the MySQL database, and display the results.

### Example

When prompted, you can ask queries like "What are the properties near the beach?" and the program will generate the SQL query to retrieve the relevant data from the database.

## Functions

### `generate_sql(user_input)`
Generates an SQL query based on user input. The schema of the database is provided as context for the GPT model to generate accurate queries.

### `execute_sql(sql_query)`
Executes the generated SQL query against the MySQL database and returns the results.

### `format_results(data, columns)`
Formats the SQL query results into a readable string for display.

### `main()`
Handles the user input, generates the SQL query, executes it, and displays the results.
