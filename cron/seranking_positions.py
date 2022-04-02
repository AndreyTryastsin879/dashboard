import requests
import json
import datetime
from datetime import timedelta

from config import *


def get_auth_headers_se_ranking():
    return {'Authorization': f'OAuth {SE_RANKING_TOKEN}'}


def get_top10_positions_se_ranking_api(project_seranking_id, date_from, date_to):
    request = requests.get(SE_RANKING_URL_TEMPLATE.format(project_seranking_id, date_from, date_to),
                 headers=get_auth_headers_se_ranking())
        
    request_data = json.loads(request.text)
    
    return request_data


def get_yandex_top10_positions_percentage_se_ranking_api(api_response):
    
    yandex_top10_positions_percentage = api_response[0]['data'][0]['value']
    
    return int(float(yandex_top10_positions_percentage))
    

def get_google_top10_positions_percentage_se_ranking_api(api_response):
    
    google_top10_positions_percentage = api_response[1]['data'][0]['value']
    
    return int(float(google_top10_positions_percentage))


def main():
    df = select_projects_by_service_id('SEO')[['name','seranking_id']]
    df.dropna(subset=['seranking_id'], inplace=True)
    df['seranking_id'] = df['seranking_id'].astype(int)

    projects_param = df.to_dict('record')

    for row in projects_param:
        project_name, project_seranking_id = row['name'], row['seranking_id']
        
        print(project_name)

        current_date = datetime.datetime.now().date()

        print(current_date)

        try:
            #Yandex
            top10_positions_api_response = get_top10_positions_se_ranking_api(project_seranking_id, current_date, current_date)

            yandex_top10_positions_percentage = get_yandex_top10_positions_percentage_se_ranking_api(top10_positions_api_response)

            insert_data_to_database(project_name, 'Yandex', 'Positions_percentage', yandex_top10_positions_percentage, current_date)

            insert_data_to_data_collecting_report(project_name, 'Yandex_positions_report', 'OK', '-', current_date, yandex_top10_positions_percentage)

        except Exception as e:
            error_mesage = get_traceback(e)
            insert_data_to_data_collecting_report(project_name, 'Yandex_positions_report', 'ERROR', error_mesage, current_date, '-')
                
        try:
            #Google
            top10_positions_api_response = get_top10_positions_se_ranking_api(project_seranking_id, current_date, current_date)

            google_top10_positions_percentage = get_google_top10_positions_percentage_se_ranking_api(top10_positions_api_response)
            
            insert_data_to_database(project_name, 'Google', 'Google_positions_report', google_top10_positions_percentage, current_date)
                
            insert_data_to_data_collecting_report(project_name, 'Google_positions_report', 'OK', '-', current_date, google_top10_positions_percentage)
            
        except Exception as e:
            error_mesage = get_traceback(e)
            insert_data_to_data_collecting_report(project_name, 'Google_positions_report', 'ERROR', error_mesage, current_date, '-')
        

if __name__ == '__main__':
    main()