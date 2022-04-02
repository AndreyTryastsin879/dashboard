import requests
import json
import datetime
from datetime import timedelta

from config import *


def last_day_of_month(any_day):
    next_month = any_day.replace(day=28) + datetime.timedelta(days=4)  # this will never fail
    return next_month - datetime.timedelta(days=next_month.day)


def get_auth_headers() -> dict:
    return {'Authorization': f'OAuth {YANDEX_TOKEN}'}


def get_webmaster_user_id() -> str:
    r = requests.get(WEBMASTER_USERID_URL, headers=get_auth_headers())
    user_id = json.loads(r.text)['user_id']
    return user_id


def webmaster_get_params(start_period_date, finish_period_date):
    return {
    'date_from': start_period_date,
    'date_to': finish_period_date
    }


def get_quantity_of_pages_webmaster_api(user_id, project_yandex_webmaster_host, start_period_date, finish_period_date):
    
    user_id = get_webmaster_user_id()
    
    request = requests.get(WEBMASTER_URL_TEMPLATE.format(user_id, project_yandex_webmaster_host),
                           headers=get_auth_headers(),
                           params=webmaster_get_params(start_period_date, finish_period_date))
                    
    request_data = json.loads(request.text)
    
    return request_data['history']


def main():
    df = select_projects_by_service_id('SEO')[['name','yandex_webmaster_host']]
    df.dropna(subset=['yandex_webmaster_host'], inplace=True)

    projects_param = df.to_dict('record')

    user_id = get_webmaster_user_id()

    for row in projects_param:
        project_name, project_yandex_webmaster_host = row['name'], row['yandex_webmaster_host']
        
        print(project_name)
        
        current_date = datetime.datetime.now().date()

        print(current_date)
        
        first_month_day = datetime.date(current_date.year, current_date.month, 1)
        last_month_day = last_day_of_month(first_month_day)
        
        if current_date == first_month_day:
            break
        
        if current_date > first_month_day:
            
            start_period_date = datetime.date(current_date.year, current_date.month, current_date.day-1)
            finish_period_date = current_date

            print(start_period_date, finish_period_date)

            try:
                project_indexed_pages_quantity = get_quantity_of_pages_webmaster_api(user_id, project_yandex_webmaster_host, start_period_date, finish_period_date)
                print(project_indexed_pages_quantity[0]['value']) 
                if len(project_indexed_pages_quantity) > 0:
                    insert_data_to_database(project_name,
                                            'Yandex',
                                            'Yandex_indexed_pages_quantity', 
                                            project_indexed_pages_quantity[0]['value'], 
                                            current_date)
                    
                    insert_data_to_data_collecting_report(project_name, 'Yandex_indexed_pages_quantity',
                                                          'OK', '-', current_date, project_indexed_pages_quantity[0]['value'])
                    
                if len(project_indexed_pages_quantity) == 0:
                    pass
               
            except Exception as e:
            	error_mesage = get_traceback(e)
            	insert_data_to_data_collecting_report(project_name, 'Yandex_indexed_pages_quantity',
                                                    'ERROR', error_mesage, current_date, '-')

if __name__ == '__main__':
    main()