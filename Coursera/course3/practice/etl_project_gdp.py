import pandas as pd, requests, sqlite3 as sql3
from datetime import datetime
from bs4 import BeautifulSoup



def extract_from_web(url : str, attributes : list) -> pd.DataFrame:
    """
    This function extracts the required information (the table)
    from the website into a dataframe variable
    Parameters:
        url (str): The URL of the webpage containing the required table.
        attributes (list): A list containing the name of the columns of the dataframe.
    Returns:
        pd.DataFrame: DataFrame containing the extracted GDP table data.
    """
    
    r = requests.get(url)
    html_text_parsed = BeautifulSoup(r.text, 'html.parser')
    all_table = html_text_parsed.find_all('tbody')
    target_table = all_table[2]

    rows = target_table.find_all('tr')
    df = pd.DataFrame(columns=attributes)
    for row in rows:
        td_data = row.find_all('td')
        if len(td_data) != 0:
            if td_data[0].find('a') is not None and td_data[2].get_text(strip=True) != '—':
                i = 0
                data = pd.DataFrame([{'Country': td_data[0].a.get_text(strip=True),
                        'GDP_USD_millions': td_data[2].get_text(strip=True)
                    }])
                df = pd.concat([df, data], ignore_index=True)
    return df

def transform(df : pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the input DataFrame by applying necessary data cleaning and processing steps
    required for the ETL pipeline.

    Args:
        df (pd.DataFrame): The input DataFrame containing raw GDP data.

    Returns:
        pd.DataFrame: The transformed DataFrame ready for loading or further analysis.
    """
    
    # transform to float
    gdp = df['GDP_USD_millions']
    gdp = gdp.apply(lambda x: x.split(','))
    gdp = gdp.apply(lambda x: float(''.join(x)))
    
    # Divide and round to 2 decimal places
    gdp = gdp.apply(lambda x : round(x / 1000, 2))
    df['GDP_USD_millions'] = gdp
    df = df.rename(columns={'GDP_USD_millions': 'GDP_USD_billions'})
    return df

def load_to_csv(df : pd.DataFrame, target_file : str) -> None:
    """
    This function saves the transformed dataframe to csv target file
    Parameters:
        df (pd.DataFrame): Transformed and finalized GDP data.
        target_file (str): The path to the target csv file where GDP info will be saved
    Returns:
        None
    """
    df.to_csv(target_file)
    return None

def load_to_db(df :pd.DataFrame, db_name : str, table_name : str) -> None:
    """
    Loads a pandas DataFrame into a specified table within a database.
    Args:
        df (pd.DataFrame): The DataFrame containing the data to be loaded.
        db_name (str): The name or path of the target database.
        table_name (str): The name of the table where data will be inserted.
    Returns:
        None
    """
    db = sql3.connect(db_name)
    df.to_sql(table_name, db, if_exists='replace', index=False)
    db.close()
    return None

def query_database(db_name : str, query_statement : str) -> None:
    db = sql3.connect(db_name)
    output = pd.read_sql(query_statement, db)
    print(output)
    db.close()

def log_progress(message, log_file) -> None:
    """
    Logs a message to the specified log file.
    Args:
        message (str): The message to be logged.
        log_file (str): The path to the log file where the message will be written.
    Returns:
        None
    """
    timestamp_format = '%Y-%h-%d-%H:%M:%S' # Year-Monthname-Day-Hour-Minute-Second 
    now = datetime.now() # get current timestamp 
    timestamp = now.strftime(timestamp_format) 
    with open("./etl_project_log.txt","a") as f: 
        f.write(timestamp + ' : ' + message + '\n')



if __name__ == '__main__':
    url = 'https://web.archive.org/web/20230902185326/https://en.wikipedia.org/wiki/List_of_countries_by_GDP_%28nominal%29'

    target_file = 'countries_by_GDP.csv'
    log_file = 'etl_project_log.txt'
    db_name = 'world_economies.db'
    table_name = 'countries_by_GDP'
    attributes = ['Country', 'GDP_USD_millions']


    # EXTRACT
    log_progress('Preliminaries complete. Initiating ETL process', log_file)
    df = extract_from_web(url, attributes)

    # TRANSFORM
    log_progress('Data extraction complete. Initiating Transformation process', log_file)
    transformed_df = transform(df)

    # LOAD
    log_progress('Data transformation complete. Initiating loading process', log_file)
    load_to_csv(df, target_file)
    log_progress('Data saved to CSV file', log_file)

    load_to_db(transformed_df, db_name, table_name)
    log_progress('Data loaded to Database as table. Running the query', log_file)

    # Query
    query = f"SELECT * from {table_name} WHERE GDP_USD_billions >= 100"
    query_database(db_name, query)

    log_progress('Process Complete.', log_file)