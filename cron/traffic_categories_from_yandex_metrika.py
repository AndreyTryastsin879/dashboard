import requests
import json
import datetime
from datetime import timedelta
import time
import re

import pandas as pd

from config import *
from traffic_categories_templates import *


LIMIT = 100000
DIMENSIONS = 'ym:s:startURL'
METRICS = 'ym:s:visits'
FILTERS = "ym:s:trafficSource=='organic'"


def insert_seo_traffic_categories_data_to_database(project_name, traffic_category, value, current_date, month_year):
    query = db.insert(seo_traffic_categories).values(project_name = project_name,
                                                    traffic_category = traffic_category, 
                                                    value = value, 
                                                    created = current_date,
                                                    month_year = month_year)  
    ResultProxy = connection.execute(query)


def last_day_of_month(any_day):
    next_month = any_day.replace(day=28) + datetime.timedelta(days=4)  # this will never fail
    return next_month - datetime.timedelta(days=next_month.day)


def get_auth_headers():
    return {'Authorization': f'OAuth {YANDEX_TOKEN}'}


def metrika_get_params(first_month_day, last_month_day, project_yandex_metrika_counter_id):
    return {
                    'id': project_yandex_metrika_counter_id,
                    'date1': first_month_day.strftime('%Y-%m-%d'),
                    'date2': last_month_day.strftime('%Y-%m-%d'),
                    'limit': LIMIT,
                    'dimensions': DIMENSIONS,
                    'metrics': METRICS,
                    'filters': FILTERS
                }


def get_search_engine_start_urls_data_from_metrika_api(first_month_day, last_month_day, project_yandex_metrika_counter_id):
    request = requests.get(METRIKA_URL_TEMPLATE,
                           headers=get_auth_headers(),
                           params=metrika_get_params(first_month_day, last_month_day, project_yandex_metrika_counter_id))
                
    request_data = json.loads(request.text)
    
    return request_data['data']


def extract_urls_and_visits_quantity(data):
    pages_list = []
    visits = []
    for element in range(len(data)):
        pages_list.append(data[element]['dimensions'][0]['name'])
        visits.append(data[element]['metrics'][0])
        
    df = pd.DataFrame(pages_list,columns=['urls'])
    df['visits_quantity'] = visits
    df['visits_quantity'] = df['visits_quantity'].astype(int)
    
    return df


def take_traffic_category_and_visits_and_insert_to_database(project_name, current_date, last_month_day, dictionary):
    for row in dictionary:
        traffic_category, visits_quantity = row['traffic_category'], row['visits_quantity']
        insert_seo_traffic_categories_data_to_database(project_name,
                                                       traffic_category,
                                                       visits_quantity,
                                                       current_date,
                                                       month_year = last_month_day.strftime('%B %Y')
                                                      )
        
        insert_data_to_data_collecting_report(project_name, 'Traffic_categories_report',
                                             'OK', '-', current_date, '-')
       


def main():
    df = select_projects_by_service_id('SEO')[['name','yandex_metrika_counter_id']]
    df.dropna(subset=['yandex_metrika_counter_id'], inplace=True)
    df['yandex_metrika_counter_id'] = df['yandex_metrika_counter_id'].astype(int)

    projects_param = df.to_dict('record')

    for row in projects_param:
        try:
            project_name, project_yandex_metrika_counter_id = row['name'], row['yandex_metrika_counter_id']

            print(project_name)

            #current_date = datetime.datetime.now()
            current_date = datetime.date(2023,7,1)

            print(current_date)

            first_month_day = datetime.date(current_date.year, current_date.month-1, 1)
            last_month_day = last_day_of_month(first_month_day)

            print(first_month_day, last_month_day)


            data_from_metrika = get_search_engine_start_urls_data_from_metrika_api(first_month_day, last_month_day, project_yandex_metrika_counter_id)

            df = extract_urls_and_visits_quantity(data_from_metrika)

            try:
                # if project_name == 'Megaposm':
                #     list_of_dicts = megaposm(df)
                #     print(list_of_dicts)
                #     take_traffic_category_and_visits_and_insert_to_database(project_name, current_date, last_month_day, list_of_dicts)

                if project_name == 'Frutoss':
                    list_of_dicts = frutoss(df)
                    print(list_of_dicts)
                    take_traffic_category_and_visits_and_insert_to_database(project_name, current_date, last_month_day, list_of_dicts)

                # if project_name == 'Mentalshop':
                #     list_of_dicts = mentalshop(df)
                #     print(list_of_dicts)
                #     take_traffic_category_and_visits_and_insert_to_database(project_name, current_date, last_month_day, list_of_dicts)
                #
                # if project_name == 'Da-Vita':
                #     list_of_dicts = davita(df)
                #     take_traffic_category_and_visits_and_insert_to_database(project_name, current_date, last_month_day, list_of_dicts)
                #
                # if project_name == 'Guinot':
                #     list_of_dicts = guinot(df)
                #     take_traffic_category_and_visits_and_insert_to_database(project_name, current_date, last_month_day, list_of_dicts)

                if project_name == 'Big-Bears':
                    list_of_dicts = bigbears(df)
                    take_traffic_category_and_visits_and_insert_to_database(project_name, current_date, last_month_day, list_of_dicts)

                # # if project_name == 'Flexfit':
                # #     list_of_dicts = flexfit(df)
                # #     take_traffic_category_and_visits_and_insert_to_database(project_name, current_date, last_month_day, list_of_dicts)
                # #
                # # if project_name == 'Certex':
                # #     list_of_dicts = certex(df)
                # #     take_traffic_category_and_visits_and_insert_to_database(project_name, current_date, last_month_day, list_of_dicts)
                #
                # if project_name == 'Inauto':
                #     list_of_dicts = inauto(df)
                #     take_traffic_category_and_visits_and_insert_to_database(project_name, current_date, last_month_day, list_of_dicts)

                if project_name == 'Skurala':
                    list_of_dicts = skurala(df)
                    take_traffic_category_and_visits_and_insert_to_database(project_name, current_date, last_month_day, list_of_dicts)

                if project_name == 'Elitewheels':
                    list_of_dicts = elitewheels(df)
                    take_traffic_category_and_visits_and_insert_to_database(project_name, current_date, last_month_day, list_of_dicts)

                if project_name == 'Elitewheels-Msk':
                    list_of_dicts = elitewheels_msk(df)
                    take_traffic_category_and_visits_and_insert_to_database(project_name, current_date, last_month_day, list_of_dicts)

                if project_name == 'Kolesa-V-Pitere':
                    list_of_dicts = kvp(df)
                    take_traffic_category_and_visits_and_insert_to_database(project_name, current_date, last_month_day, list_of_dicts)

                if project_name == 'The-Koleso':
                    list_of_dicts = koleso(df)
                    take_traffic_category_and_visits_and_insert_to_database(project_name, current_date, last_month_day, list_of_dicts)

                if project_name == 'Kypishiny':
                    list_of_dicts = kypishiny(df)
                    take_traffic_category_and_visits_and_insert_to_database(project_name, current_date, last_month_day, list_of_dicts)

            except Exception as e:
                error_mesage = get_traceback(e)
                insert_data_to_data_collecting_report(project_name, 'Traffic_categories_report',
                                                          'ERROR', error_mesage, current_date, '-')
        except Exception as e:
            error_mesage = get_traceback(e)
            insert_data_to_data_collecting_report(project_name, 'Traffic_categories_report',
                                                  'ERROR', error_mesage, current_date, '-')

if __name__ == '__main__':
    main()