import streamlit as st
from openai import AzureOpenAI  # Importing OpenAI library to interact with the GPT model
import mysql.connector  # Importing MySQL connector to interact with the database
from dotenv import load_dotenv  # Importing dotenv to load environment variables from a .env file
import pandas as pd  # For displaying query results in a table
import os  # For accessing environment variables

# Load environment variables from the .env file
load_dotenv()
API_KEY = os.getenv('api_key')  # Fetch API key from environment variables
API_VERSION = os.getenv('api_version')  # Fetch API version from environment variables
API_ENDPOINT = os.getenv('api_endpoint')  # Fetch API version from environment variables
HOST = os.getenv('host')  # Fetch the host for MySQL connection
USER = os.getenv('user')  # Fetch the user for MySQL connection
PASSWORD = os.getenv('password')  # Fetch the password for MySQL connection
DATABASE = os.getenv('database_name')  # Fetch the database name for MySQL connection

# Initialize OpenAI client with the API key
client = AzureOpenAI(
    api_key=API_KEY,
    api_version=API_VERSION,
    azure_endpoint=API_ENDPOINT
)

# Establish connection to MySQL database
db_connection = mysql.connector.connect(
    host=HOST,
    user=USER,
    password=PASSWORD,
    database=DATABASE
)
cursor = db_connection.cursor()  # Create a cursor object to interact with the database


def generate_sql(user_input):
    """Generate SQL query using ChatGPT based on user input."""
    schema_description = (
        "Field\tType\tNull\tKey\tDefault\n"
        "last_update\ttext\tYES\t\tNULL\n"
        "reference_number\ttext\tYES\t\tNULL\n"
        "permit_number\ttext\tYES\t\tNULL\n"
        "offering_type\ttext\tYES\t\tNULL\n"
        "property_type\ttext\tYES\t\tNULL\n"
        "price_on_application\ttext\tYES\t\tNULL\n"
        "price\ttext\tYES\t\tNULL\n"
        "payment_method\ttext\tYES\t\tNULL\n"
        "down_payment_price\ttext\tYES\t\tNULL\n"
        "service_charge\ttext\tYES\t\tNULL\n"
        "cheques\ttext\tYES\t\tNULL\n"
        "city\ttext\tYES\t\tNULL\n"
        "community\ttext\tYES\t\tNULL\n"
        "sub_community\ttext\tYES\t\tNULL\n"
        "property_name\ttext\tYES\t\tNULL\n"
        "title_en\ttext\tYES\t\tNULL\n"
        "title_ar\ttext\tYES\t\tNULL\n"
        "description_en\ttext\tYES\t\tNULL\n"
        "description_ar\ttext\tYES\t\tNULL\n"
        "private_amenities\ttext\tYES\t\tNULL\n"
        "commercial_amenities\ttext\tYES\t\tNULL\n"
        "plot_size\ttext\tYES\t\tNULL\n"
        "size\tint\tYES\t\tNULL\n"
        "bedroom\tint\tYES\t\tNULL\n"
        "bathroom\ttext\tYES\t\tNULL\n"
        "agent_id\tint\tYES\t\tNULL\n"
        "agent_name\ttext\tYES\t\tNULL\n"
        "agent_email\ttext\tYES\t\tNULL\n"
        "agent_phone\tbigint\tYES\t\tNULL\n"
        "developer\ttext\tYES\t\tNULL\n"
        "build_year\ttext\tYES\t\tNULL\n"
        "completion_status\ttext\tYES\t\tNULL\n"
        "floor\ttext\tYES\t\tNULL\n"
        "stories\ttext\tYES\t\tNULL\n"
        "parking\ttext\tYES\t\tNULL\n"
        "furnished\ttext\tYES\t\tNULL\n"
        "view360\ttext\tYES\t\tNULL\n"
        "video_tour_url\ttext\tYES\t\tNULL\n"
        "photos\ttext\tYES\t\tNULL\n"
    )
    prompt = (
        f"{schema_description}\n"
        "Analyze this schema thoroughly and understand the data types and their relationships.\n"
        "From now on, I will provide user inputs, and you must generate SQL queries based on this schema.\n"
        "Use your knowledge and any available fields to craft accurate, optimized queries.\n"
        "\n"
        "Guidelines:\n"
        "1. Use every relevant field to enhance query precision.\n"
        "2. If the user input mentions locations, incorporate geographical knowledge of UAE.\n"
        "   For instance, beaches should include popular ones like 'Jumeirah Beach', 'Turtle Beach', etc., and nearby properties.\n"
        "3. For fields like 'price' (stored as text), convert it to numeric using `CAST` for comparisons.\n"
        "4. For 'bathroom', use queries like `bathroom LIKE '3%'` to match text patterns.\n"
        "5. Ignore 'property_type' unless explicitly instructed, as it’s not a reliable indicator of property type.\n"
        "6. Return detailed property information rather than just counts.\n"
        "7. Focus on vivid and thorough searches; the query size doesn’t matter as long as it's efficient.\n"
        "\n"
        "Special notes:\n"
        "- Assume data is UAE-specific and prioritize accuracy.\n"
        "- Always validate fields for meaningful conditions.\n"
        "- For ambiguous inputs, make assumptions based on general real-estate knowledge in UAE.\n"
        "- MAKE SURE YOU ALWAYS RETURN JUST AN SQL QUERY AND NOTHING ELSE BECAUSE WHATEVER YOU RETURN WILL DIRECTLY BE PASSED TO SQL.\n"
        "\n"
        f"User Input: {user_input}"
    )

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    sql_query = response.choices[0].message.content.strip().replace("```sql", "").replace("```", "").strip()
    return sql_query


def execute_sql(sql_query):
    """Execute the generated SQL query and fetch results."""
    try:
        cursor.execute(sql_query)
        return cursor.fetchall(), cursor.column_names  # Fetch data and column names
    except mysql.connector.Error as err:
        st.error(f"SQL Error: {err}")
        return None, None


# Streamlit frontend
def main():
    st.title("Properties GPT Wrapper")
    st.subheader("Search for properties using natural language")

    user_input = st.text_input("Enter your search query:")

    if user_input:
        sql_query = generate_sql(user_input)  # Generate SQL query based on user input
        st.code(sql_query, language="sql")  # Display the generated SQL query

        results, columns = execute_sql(sql_query)  # Execute query and fetch results

        if results:
            df = pd.DataFrame(results, columns=columns)  # Convert results to a DataFrame
            st.dataframe(df)  # Display the DataFrame
        else:
            st.warning("No data found or an error occurred.")


if __name__ == "__main__":
    main()
