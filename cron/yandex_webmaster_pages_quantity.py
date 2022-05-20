import requests
import json
import datetime
from datetime import timedelta

from config import *


def get_auth_headers():
    return {'Authorization': f'OAuth {YANDEX_TOKEN}'}


def get_webmaster_user_id():
    r = requests.get(WEBMASTER_USERID_URL, headers=get_auth_headers())
    user_id = json.loads(r.text)['user_id']
    return user_id


def webmaster_get_params(start_period_date, finish_period_date):
   return {
       'date_from': start_period_date.strftime('%Y-%m-%d'),
       'date_to': finish_period_date.strftime('%Y-%m-%d')
   }


def get_quantity_of_pages_webmaster_api(user_id, project_yandex_webmaster_host, start_period_date, finish_period_date):
    request = requests.get(WEBMASTER_URL_TEMPLATE.format(user_id, project_yandex_webmaster_host),
                           headers=get_auth_headers(), params=webmaster_get_params(start_period_date, finish_period_date))

    request_data = json.loads(request.text)

    return request_data['history']


def main():
    df = select_projects_by_service_id('SEO')[['name', 'yandex_webmaster_host']]
    df.dropna(subset=['yandex_webmaster_host'], inplace=True)

    projects_param = df.to_dict('record')

    user_id = get_webmaster_user_id()


    for row in projects_param:
        project_name, project_yandex_webmaster_host = row['name'], row['yandex_webmaster_host']

        print(project_name)

        current_date = datetime.datetime.now()

        yandex_indexed_pages_quantity_next_date_after_last_date = yandex_indexed_pages_quantity_last_date - timedelta(days=1)

        print(current_date.date(), yandex_indexed_pages_quantity_next_date_after_last_date.date())

        try:

            project_indexed_pages_quantity = get_quantity_of_pages_webmaster_api(user_id,
                                                                                 project_yandex_webmaster_host,
                                                                                 yandex_indexed_pages_quantity_next_date_after_last_date,
                                                                                 current_date)

            for element in range(len(project_indexed_pages_quantity)):
                print(datetime.datetime.fromisoformat(project_indexed_pages_quantity[element]['date']).date(),
                      project_indexed_pages_quantity[element]['value'])


                report_date = datetime.datetime.fromisoformat(project_indexed_pages_quantity[element]['date']).date()
                report_value = project_indexed_pages_quantity[element]['value']

                insert_data_to_database(project_name,
                                        'Yandex',
                                        'Yandex_indexed_pages_quantity',
                                        report_value,
                                        report_date)

                insert_data_to_data_collecting_report(project_name, 'Yandex_indexed_pages_quantity',
                                                      'OK', '-', current_date, report_value)

        except Exception as e:
            error_mesage = get_traceback(e)
            insert_data_to_data_collecting_report(project_name, 'Yandex_indexed_pages_quantity',
                                                  'ERROR', error_mesage, current_date, '-')

if __name__ == '__main__':
    main()
