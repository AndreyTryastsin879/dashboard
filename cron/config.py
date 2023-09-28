import sqlalchemy as db

import traceback

import pandas as pd

from settings import DB_PASS, DB_HOST, DB_PORT, DB_USER, DB_NAME

engine = db.create_engine(f'mysql+mysqlconnector://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}')
connection = engine.connect()
metadata = db.MetaData()

projects = db.Table('project', metadata, autoload=True, autoload_with=engine)
seo_data_linear_plots = db.Table('seo_data_for_linear_plots', metadata, autoload=True, autoload_with=engine)
seo_traffic_categories = db.Table('seo_traffic_categories', metadata, autoload=True, autoload_with=engine)
data_collecting_report = db.Table('data_collecting_report', metadata, autoload=True, autoload_with=engine)
projects_services = db.Table('projects_services', metadata, autoload=True, autoload_with=engine)
service = db.Table('service', metadata, autoload=True, autoload_with=engine)


YANDEX_TOKEN = 'y0_AgAAAAASqca9AAaElQAAAADtwtOHqHYv0NvJS0qZ1p6o9nf1ahUjYcQ'

WEBMASTER_URL_TEMPLATE = 'https://api.webmaster.yandex.net/v4/user/{}/hosts/{}/search-urls/in-search/history'

WEBMASTER_USERID_URL = 'https://api.webmaster.yandex.net/v4/user'

METRIKA_URL_TEMPLATE = 'https://api-metrika.yandex.net/stat/v1/data'

SE_RANKING_URL_TEMPLATE = 'https://api4.seranking.com/sites/{}/chart?date_from={}&date_to={}&type=top10_percent'

SE_RANKING_TOKEN = '389fcf289305f9df5193be0f95c688d40e332273'


def insert_data_to_database(project_name, data_source, data_type, value, current_date):
    query = db.insert(seo_data_linear_plots).values(project_name = project_name,
                                                    data_source = data_source,
                                                    data_type = data_type, 
                                                    value = value, 
                                                    created = current_date)  
    ResultProxy = connection.execute(query)


def insert_data_to_data_collecting_report(project_name, report_name, status, error_text, current_date, value):
    query = db.insert(data_collecting_report).values(project_name = project_name,
                                                    report_name = report_name,
                                                    status = status, 
                                                    error_text = error_text, 
                                                    created = current_date,
                                                    value = value)  
    ResultProxy = connection.execute(query)


def select_projects_by_service_id(service_name):
    # получение id услуги по названию услуги
    seo_service_data = connection.execute(db.select([service]).where(service.columns.name == service_name)).fetchall()
    seo_service_id = seo_service_data[0][0]
    # получение id проектов по id услуги
    seo_projects_id_tuple = connection.execute(db.select([projects_services])
                                              .where(projects_services.columns.service_id == seo_service_id)
                                             ).fetchall()
    
    seo_projects_id_list = [element[0] for element in seo_projects_id_tuple]
    
    # срез данных о проектах по id проектов, которые относятся к услуге
    projects_params = connection.execute(db.select([projects])).fetchall()
    df = pd.DataFrame(projects_params)
    df.columns = projects_params[0].keys()
    
    df = df[df['id'].isin(seo_projects_id_list)]
    
    return df


def get_traceback(e):
    lines = traceback.format_exception(type(e), e, e.__traceback__)
    return ''.join(lines)


ResultSet = (
        connection.execute(db.select([seo_data_linear_plots])
                           .where(seo_data_linear_plots.columns.data_type == 'Yandex_indexed_pages_quantity')
                           .order_by(db.desc(seo_data_linear_plots.columns.created))
                           .limit(1)).fetchall()
    )


yandex_indexed_pages_quantity_last_date = ResultSet[0][4]