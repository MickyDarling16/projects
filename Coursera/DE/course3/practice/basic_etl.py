import glob
import pandas as pd
from datetime import datetime
import xml.etree.ElementTree as ET

log_file = 'log_file.txt'
target_file = 'transformed.csv'

def extract_from_csv(csv_file):
    return pd.read_csv(csv_file)

def extract_from_json(json_file):
    return pd.read_json(json_file, lines=True)

def extract_from_xml(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    name = []
    height = []
    weight = []
    df = pd.DataFrame(columns = ['name', 'height', 'weight'])

    for person in root:
        name.append(person.find('name').text)
        height.append(float(person.find('height').text))
        weight.append(float(person.find('weight').text))
    
    data = pd.DataFrame({'name' : name, 'height' : height, 'weight' : weight})
    df = pd.concat([df, data], ignore_index=True)
    return df


def extract():
    extracted_data_so_far = pd.DataFrame(columns = ['name', 'height', 'weight'])

    # Extract all csv files into transformed_data.csv
    for csvfile in glob.glob('*.csv'):
        if csvfile != target_file:
            extracted_csv = extract_from_csv(csvfile)
            extracted_data_so_far = pd.concat([extracted_data_so_far, extracted_csv], ignore_index=True)
    
    # Extract all json files into transformed_data.csv
    for jsonfile in glob.glob('*.json'):
        extracted_json = extract_from_json(jsonfile)
        extracted_data_so_far = pd.concat([extracted_data_so_far, extracted_json], ignore_index=True)

    # Extract all xml files into transformed_data.csv
    for xmlfile in glob.glob('*.xml'):
        extracted_xml = extract_from_xml(xmlfile)
        extracted_data_so_far = pd.concat([extracted_data_so_far, extracted_xml], ignore_index=True)
    
    return extracted_data_so_far


extracted_data = extract()
# print(extracted_data)


def transform(data):
    '''
    Convert inches to meters and pounds to kilograms and round to 2 decimal places
    '''
    
    # Inches to meter
    data['height'] = round(data['height'] * 0.0254, 2)

    # Pounds to kilograms
    data['weight'] = round(data['weight'] * 0.45359237, 2)

    return data

# print(transform(extracted_data))

def load_data(target_file, transformed_data):
    transformed_data.to_csv(target_file)

def log_progress(message):
    timestamp_format = '%Y-%h-%d-%H:%M:%S'  # Year-Monthname-Day-Hour-Minute-Second
    
    now = datetime.now() #current timestamp
    timestamp = now.strftime(timestamp_format) # Format 'now' variable to meet custom form
    with open(log_file, 'a') as logfile:
        logfile.write(f'{timestamp}: {message}\n')


if __name__ == '__main__':
    # Log the initialization of the ETL process 
    log_progress("ETL Job Started") 
    
    # Log the beginning of the Extraction process 
    log_progress("Extract phase Started") 
    extracted_data = extract() 
    
    # Log the completion of the Extraction process 
    log_progress("Extract phase Ended") 
    
    # Log the beginning of the Transformation process 
    log_progress("Transform phase Started") 
    transformed_data = transform(extracted_data) 
    print("Transformed Data") 
    print(transformed_data) 
    
    # Log the completion of the Transformation process 
    log_progress("Transform phase Ended") 
    
    # Log the beginning of the Loading process 
    log_progress("Load phase Started") 
    load_data(target_file,transformed_data) 
    
    # Log the completion of the Loading process 
    log_progress("Load phase Ended") 
    
    # Log the completion of the ETL process 
    log_progress("ETL Job Ended\n")