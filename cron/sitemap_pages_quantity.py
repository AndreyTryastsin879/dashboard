import requests
import json
import datetime
from datetime import timedelta
import time
import re

from bs4 import BeautifulSoup

from config import *

user_agent = {'User-agent': 'Mozilla/5.0'}

def parse_mono_sitemap(beautiful_soup):
    url_list = []
    for url in beautiful_soup.find_all('loc'):
        url_list.append(url.text)
            
    return url_list


def parse_multi_sitemap(beautiful_soup):
    maps = []
    for sitemap in beautiful_soup.find_all('loc'):
        maps.append(sitemap.text)

    url_list = []
    for map_number in range(len(maps)):
        request = requests.get(maps[map_number], headers=user_agent)
        time.sleep(2)
        soup = BeautifulSoup(request.text, 'lxml')
        for url in soup.find_all('loc'):
            url_list.append(url.text)
            
    return url_list


def check_multi_or_mono_sitemap(soup_sitemap):
    if len(re.findall('sitemapindex',str(soup_sitemap))) > 0:
        return parse_multi_sitemap(soup_sitemap)
        
    else:
        return parse_mono_sitemap(soup_sitemap)


def main():
    df = select_projects_by_service_id('SEO')[['name','sitemap_path','second_sitemap_path']]
    df.dropna(subset=['sitemap_path'], inplace=True)

    projects_param = df.to_dict('record')

    for row in projects_param:
        project_name, project_sitemap_path, project_second_sitemap_path = row['name'], row['sitemap_path'], row['second_sitemap_path']
        print(project_name)
        print(project_sitemap_path)
        print(project_second_sitemap_path)

        current_date = datetime.datetime.now()
        try:
            if project_second_sitemap_path == None:
                request = requests.get(project_sitemap_path, headers=user_agent)
                soup_sitemap = BeautifulSoup(request.text, 'lxml')

                url_list = check_multi_or_mono_sitemap(soup_sitemap)

                value = len(url_list)
                print(value)
                insert_data_to_database(project_name, 'Sitemap', 'Pages_quantity_in_sitemap', value, current_date)
                insert_data_to_data_collecting_report(project_name, 'Pages_quantity_in_sitemap',
                                                  'OK', '-', current_date, value)

            if project_second_sitemap_path != None:
                request_first_sitemap = requests.get(project_sitemap_path, headers=user_agent)
                soup_first_sitemap = BeautifulSoup(request.text, 'lxml')

                first_sitemap_url_list = check_multi_or_mono_sitemap(soup_first_sitemap)

                request_second_sitemap = requests.get(project_second_sitemap_path, headers=user_agent)
                soup_second_sitemap = BeautifulSoup(request_second_sitemap.text, 'lxml')

                second_sitemap_url_list = check_multi_or_mono_sitemap(soup_second_sitemap)

                value = len(first_sitemap_url_list)+len(second_sitemap_url_list)
                print(value)
                insert_data_to_database(project_name, 'Sitemap', 'Pages_quantity_in_sitemap', value, current_date)
                insert_data_to_data_collecting_report(project_name, 'Pages_quantity_in_sitemap',
                                                  'OK', '-', current_date, value)
        except Exception as e:
            error_mesage = get_traceback(e)
            insert_data_to_data_collecting_report(project_name, 'Pages_quantity_in_sitemap',
                                                  'ERROR', error_mesage, current_date, '-')


if __name__ == '__main__':
    main()