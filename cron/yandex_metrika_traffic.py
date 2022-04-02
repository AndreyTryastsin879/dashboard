import requests
import json
import datetime
from datetime import timedelta

from cron.config import *

LIMIT = 100000
DIMENSIONS = 'ym:s:searchEngine'
ATTRIBUTION = 'cross_device_last_significant'
METRICS = 'ym:s:visits'
FILTERS = "ym:s:SearchEngineName=*'{}*'"


def get_auth_headers():
    return {'Authorization': f'OAuth {YANDEX_TOKEN}'}


def metrika_get_params(current_date, search_engine_name, project_yandex_metrika_counter_id):
    return {
                    'id': project_yandex_metrika_counter_id,
                    'date1': current_date.strftime('%Y-%m-%d'),
                    'date2': current_date.strftime('%Y-%m-%d'),
                    'limit': LIMIT,
                    'dimensions': DIMENSIONS,
                    'attribution': ATTRIBUTION,
                    'sampled': False,
                    'metrics': METRICS,
                    'filters': FILTERS.format(search_engine_name)
                }


def get_search_engine_data_from_metrika_api(current_date, search_engine_name, project_yandex_metrika_counter_id):
    request = requests.get(METRIKA_URL_TEMPLATE,
                           headers=get_auth_headers(),
                           params=metrika_get_params(current_date, search_engine_name, project_yandex_metrika_counter_id))
                
    request_data = json.loads(request.text)
    
    return request_data['totals']


def main():
	df = select_projects_by_service_id('SEO')[['name','yandex_metrika_counter_id']]
	df.dropna(subset=['yandex_metrika_counter_id'], inplace=True)
	df['yandex_metrika_counter_id'] = df['yandex_metrika_counter_id'].astype(int)

	projects_param = df.to_dict('record')

	for row in projects_param:
	    project_name, project_yandex_metrika_counter_id = row['name'], row['yandex_metrika_counter_id']
	    
	    #print(project_name)
	    
	    current_date = datetime.datetime.now()
	    print(current_date)
	    
	    try:
	        #Yandex
	        total_from_search_engine = get_search_engine_data_from_metrika_api(current_date, 'Yandex', project_yandex_metrika_counter_id)

	        total_from_yandex_engine = int(total_from_search_engine[0])

	        print(total_from_yandex_engine)

	        insert_data_to_database(project_name, 'Yandex', 'Traffic', total_from_yandex_engine, current_date)

	        insert_data_to_data_collecting_report(project_name, 'Yandex_traffic_metrika_report',
	                                              'OK', '-', current_date, total_from_yandex_engine)
	    except Exception as e:
	        error_mesage = get_traceback(e)
	        insert_data_to_data_collecting_report(project_name, 'Yandex_traffic_metrika_report',
	                                              'ERROR', error_mesage, current_date, '-')
	        
	    try:
	        #Google
	        total_from_search_engine = get_search_engine_data_from_metrika_api(current_date, 'Google', project_yandex_metrika_counter_id)
	          
	        total_from_google_engine = int(total_from_search_engine[0])

	        print(total_from_google_engine)
	                
	        insert_data_to_database(project_name, 'Google', 'Traffic', total_from_google_engine, current_date)
	        
	        insert_data_to_data_collecting_report(project_name, 'Google_traffic_metrika_report',
	        									  'OK', '-', current_date, total_from_google_engine)
	    except Exception as e:
	        error_mesage = get_traceback(e)
	        insert_data_to_data_collecting_report(project_name, 'Google_traffic_metrika_report',
	                                              'ERROR', error_mesage, current_date, '-')


if __name__ == '__main__':
	main()