import requests
import json
import datetime
from datetime import timedelta
import time
import re

from bs4 import BeautifulSoup

from cron.config import *


headers = {
    'User-agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582'
}

def main():
	df = select_projects_by_service_id('SEO')[['name','domain']]
	df.dropna(subset=['domain'], inplace=True)

	projects_param = df.to_dict('record')

	for row in projects_param:
	    project_name, project_domain = row['name'], row['domain']
	    
	    current_date = datetime.datetime.now()
	    
	    try:
	        request = requests.get(f'https://www.google.com/search?q=site:{project_domain}', headers=headers)
	        soup = BeautifulSoup(request.text, 'lxml')
	        value = soup.find_all(id = 'result-stats')[0].text.strip().split('примерно ')[1].split(' (')[0].replace('\xa0','')
	        print(value.text)
	        insert_data_to_database(project_name, 'Google', 'Google_indexed_pages_quantity', value, current_date)
	        insert_data_to_data_collecting_report(project_name, 'Google_indexed_pages_quantity',
	                                              'OK', '-', current_date, value)
	        time.sleep(10)
	    except Exception as e:
	        error_mesage = get_traceback(e)
	        insert_data_to_data_collecting_report(project_name, 'Google_indexed_pages_quantity',
	                                              'ERROR', error_mesage, current_date, '-')

if __name__ == '__main__':
    main()