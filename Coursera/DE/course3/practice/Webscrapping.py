import requests, sqlite3, pandas as pd
from bs4 import BeautifulSoup

url = 'https://web.archive.org/web/20230902185655/https://en.everybodywiki.com/100_Most_Highly-Ranked_Films'

db_name = 'Movies.db'
table_name = 'Top_50'

target_file = 'top_50_films.csv'

def extract_from_website():
    df = pd.DataFrame(columns = ['Average Rank', 'Film', 'Year'])

    count = 0

    r = requests.get(url)

    html_parsed = BeautifulSoup(r.text, 'html.parser')

    tables = html_parsed.find_all('tbody')
    target_table = tables[0]

    target_table_rows = target_table.find_all('tr')
    for row in target_table_rows:
        if count < 25:
            data = row.find_all('td')

            if len(data) != 0 and int(data[2].contents[0]) >= 2000:
                data_dict = {'Average Rank': int(data[0].contents[0]),
                            'Film': str(data[1].contents[0]),
                            'Year': int(data[2].contents[0])
                            }
                df_extracted = pd.DataFrame([data_dict])
                df = pd.concat([df, df_extracted], ignore_index=True)
                count += 1
        else:
            print(df)
            break
    
    df.to_csv(target_file) # Save locally to csv file

    sql3 = sqlite3.connect(db_name)
    df.to_sql(table_name, sql3, if_exists='replace', index=False)
    sql3.close()

extract_from_website()