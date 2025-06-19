import pandas as pd, requests, sqlite3 as sql3, datetime
from bs4 import BeautifulSoup


def extract_from_web(url, attributes) -> pd.DataFrame:
    """
    This function extracts the required information (the table)
    from the website into a dataframe variable
    Parameters:
        url (str): The URL of the webpage containing the required table.
        attributes (list): A list containing the name of the columns of the dataframe.
    Returns:
        pd.DataFrame: DataFrame containing the extracted GDP table data.
    """
    pass

def transform(df) -> pd.DataFrame:
    """
    Transforms the input DataFrame by applying necessary data cleaning and processing steps
    required for the ETL pipeline.

    Args:
        df (pd.DataFrame): The input DataFrame containing raw GDP data.

    Returns:
        pd.DataFrame: The transformed DataFrame ready for loading or further analysis.
    """
    pass

def load_to_csv(df, target_file) -> None:
    """
    This function saves the transformed dataframe to csv target file
    Parameters:
        df (pd.DataFrame): Transformed and finalized GDP data.
        target_file (str): The path to the target csv file where GDP info will be saved
    Returns:
        None
    """
    pass


def load_to_db(df, db_name, table_name) -> None:
    """
    Loads a pandas DataFrame into a specified table within a database.
    Args:
        df (pd.DataFrame): The DataFrame containing the data to be loaded.
        db_name (str): The name or path of the target database.
        table_name (str): The name of the table where data will be inserted.
    Returns:
        None
    """
    pass

def log(message, log_file) -> None:
    """
    Logs a message to the specified log file.
    Args:
        message (str): The message to be logged.
        log_file (str): The path to the log file where the message will be written.
    Returns:
        None
    """
    pass


if __name__ == '__main__':
    pass