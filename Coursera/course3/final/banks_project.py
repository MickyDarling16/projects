import pandas as pd, sqlite3 as sql3, requests
from datetime import datetime as dt
from bs4 import BeautifulSoup


def log_progress(message: str, log_file: str) -> None:
    """
    Logs a progress message to the specified log file.

    Args:
        message (str): The progress message to log.
        log_file (str): The path to the log file where the message will be written.

    Returns:
        None
    """
    timestamp_format = '%Y-%h-%d-%H:%M:%S' # Year-Monthname-Day-Hour-Minute-Second 
    now = dt.now()
    timestamp = now.strftime(timestamp_format)
    with open(log_file, 'a') as f:
        f.write(f'{timestamp} : {message}\n')

def extract(url: str, df_cols) -> pd.DataFrame:
    """
    Extracts data from the specified URL and returns it as a pandas DataFrame with the given columns.

    Args:
        url (str): The URL from which to extract data.
        df_cols (list or iterable): The list of column names for the resulting DataFrame.

    Returns:
        pd.DataFrame: A DataFrame containing the extracted data with the specified columns.
    """
    r = requests.get(url)
    html_parsed = BeautifulSoup(r.text, 'html.parser')
    all_tables = html_parsed.find_all('tbody')
    table = all_tables[0]

    rows = table.find_all('tr')

    df = pd.DataFrame(columns=df_cols)
    for row in rows:
        td_data = row.find_all('td')

        if len(td_data) != 0:
            df_data = pd.DataFrame([{'Name': td_data[1].get_text(strip=True),
                    'MC_USD_Billion': td_data[2].get_text(strip=True)
                    }])
            df = pd.concat([df, df_data], ignore_index=True)
    return df

def transform(df: pd.DataFrame, rate_csv_file_path: str) -> pd.DataFrame:
    """
    Transforms the input DataFrame using exchange rates provided in a CSV file.

    Args:
        df (pd.DataFrame): The input DataFrame to be transformed.
        rate_csv_file_path (str): Path to the CSV file containing exchange rates.

    Returns:
        pd.DataFrame: The transformed DataFrame with applied exchange rates.
    """
    rates = pd.read_csv(rate_csv_file_path)
    rates_dict = rates.set_index('Currency').to_dict()['Rate']
    df['MC_USD_Billion'] = df['MC_USD_Billion'].astype(float)
    df['MC_GBP_Billion'] = df['MC_USD_Billion'].apply(lambda x : round(rates_dict['GBP'] * x,2))
    df['MC_EUR_Billion'] = df['MC_USD_Billion'].apply(lambda x : round(rates_dict['EUR'] * x,2))
    df['MC_INR_Billion'] = df['MC_USD_Billion'].apply(lambda x : round(rates_dict['INR'] * x,2))
    print(df)
    return df

def load_to_csv(df: pd.DataFrame, output_csv_path: str) -> None:
    """
    Saves a pandas DataFrame to a CSV file.

    Args:
        df (pd.DataFrame): The DataFrame to be saved.
        output_csv_path (str): The file path where the CSV will be written.

    Returns:
        None
    """
    df.to_csv(output_csv_path)
    return None

def load_to_db(df : pd.DataFrame, sql3_connection, table_name: str) -> None:
    """
    Loads the given pandas DataFrame into a specified SQL database table.

    Args:
        df (pd.DataFrame): The DataFrame containing the data to be loaded.
        sql_connection: The SQL database connection object.
        table_name (str): The name of the table where the data will be loaded.

    Returns:
        None
    """
    df.to_sql(table_name, sql3_connection, if_exists='replace', index=False)
    return None

def run_queries(query_statements: str, sql3_connection) -> None:
    """
    Executes the provided SQL query statement using the given SQL connection.

    Args:
        query_statement (str): The SQL query to be executed.
        sql_connection: An active database connection object.

    Returns:
        None
    """
    for query in query_statements:
        print(f'\n\n{pd.read_sql_query(query, sql3_connection)}')
    return None




if __name__ == '__main__':
    url = 'https://web.archive.org/web/20230908091635/https://en.wikipedia.org/wiki/List_of_largest_banks'

    extract_cols = ['Name', 'MC_USD_Billion']

    output_csv_path = 'Largest_banks_data.csv'

    log_file_path = 'code_log.txt'
    rates_file_path = 'exchange_rate.csv'

    table_name = 'Largest_banks'
    db_name = 'Banks.db'

    queries = ['SELECT * FROM Largest_banks', 'SELECT AVG(MC_GBP_Billion) FROM Largest_banks', 'SELECT Name from Largest_banks LIMIT 5']

    log_progress('Preliminaries complete. Initiating ETL process', log_file_path)

    df = extract(url, extract_cols)
    log_progress('Data extraction complete. Initiating Transformation process', log_file_path)

    df = transform(df, rates_file_path)
    log_progress('Data transformation complete. Initiating Loading process', log_file_path)

    load_to_csv(df, output_csv_path)
    log_progress('Data saved to CSV file', log_file_path)

    connection = sql3.connect(db_name)
    load_to_db(df, connection, table_name)
    log_progress('Data loaded to Database as a table, Executing queries', log_file_path)

    run_queries(queries, connection)
    log_progress('Process Complete', log_file_path)

    connection.close()
    log_progress('Server Connection closed', log_file_path)