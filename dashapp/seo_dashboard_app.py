import pandas as pd
from datetime import datetime, timedelta

import dash
from dash import html
from dash import dcc

from dash.dependencies import Input, Output

import plotly.graph_objs as go
import plotly.express as px
from plotly.graph_objects import Layout
from plotly.validator_cache import ValidatorCache

import sqlalchemy as db

engine = db.create_engine('mysql+mysqlconnector://root:root@localhost/mrnr_dashboard_db')
connection = engine.connect()
metadata = db.MetaData()
data_table = db.Table('seo_data_for_linear_plots', metadata, autoload=True, autoload_with=engine)
traffic_categories_data_table = db.Table('seo_traffic_categories', metadata, autoload=True, autoload_with=engine)

EXTERNAL_STYLESHEET = [
    {
        "href": "https://fonts.gstatic.com",
        "rel": "preconnect"
    },
    {
        "href": "https://fonts.googleapis.com/css?family=Open+Sans:300,300i,400,400i,600,600i,700,700i|"
                "Nunito:300,300i,400,400i,600,600i,700,700i|Poppins:300,300i,400,400i,500,500i,600,600i,700,700i",
        "rel": "stylesheet"
    },
]

def linear_plot_database_to_df(data):
    if len(data)>0:
        df = pd.DataFrame(data)
        df.columns = data[0].keys()
        return df
    else:
        df = pd.DataFrame(columns=['data_source', 'data_type'])
        return df

def traffic_category_plot_database_to_df(data):
    if len(data)>0:
        df = pd.DataFrame(data)
        df.columns = data[0].keys()
        return df
    else:
        df = pd.DataFrame(columns=['month_year', 'traffic_category', 'value'])
        return df


def create_dashboard(flask_app, project):
    dashboard = dash.Dash(
        server=flask_app,
        name='SEO Dashboard',
        url_base_pathname=f'/dash/{project}/service/seo/',
        suppress_callback_exceptions=True,
        external_stylesheets=EXTERNAL_STYLESHEET,
    )

    dashboard.layout = html.Div()
    return dashboard


def get_seo_data(project):
    seo_data = connection.execute(
        db.select([data_table])
        .where(data_table.columns.project_name == project.name)
    ).fetchall()

    df = linear_plot_database_to_df(seo_data)

    return df


def create_slice(df, data_source, data_type):
    return df[(df['data_source'] == data_source) & (df['data_type'] == data_type)]


def line_plot(df, title, selector_id, graph_id):
    if len(df) > 1:
        start_date = df['created'].dt.date.min()
        end_date = df['created'].dt.date.max()

        return html.Div(
            children=[

                html.Div(
                    children=[

                        html.Div(children=[
                            html.H5(children=title, className="card-title"),

                            html.P(
                                children=f'Доступны данные за период {start_date.strftime("%B %Y")} - {end_date.strftime("%B %Y")}'),

                            html.Div(
                                children=[html.P('Временной период:')]),

                            html.Div(
                                children=[
                                    dcc.DatePickerRange(
                                        start_date=df['created'].dt.date.max() - timedelta(days=7),
                                        end_date=df['created'].dt.date.max(),
                                        display_format='DD-MM-YY',
                                        id=selector_id
                                    ),
                                ]
                            ),

                            dcc.Graph(id=graph_id),

                        ], className="card-body"

                        ),
                    ], className="card info-card customers-card"
                ),
            ], className="col-xxl-6 col-xl-12")
    else:
        pass


def line_plot_settings(dashboard, df, output, input_selector, colour, xaxis_name, yaxis_name, plot_title):
    @dashboard.callback(
        [Output(f'{output}', 'figure'),
         ],

        [Input(f'{input_selector}', 'start_date'),
         Input(f'{input_selector}', 'end_date'),
         ]
    )
    def update_figure(start_date, end_date):
        # Фильтрация данных для вывода диапазона на график
        filtered_data = df.query('created >= @start_date and created <= @end_date')

        data = [go.Scatter(x=filtered_data['created'],
                           y=filtered_data['value'],
                           mode='lines',
                           marker=dict(color=f'{colour}')
                           )
                ]

        return (
            {
                'data': data,
                'layout': go.Layout(xaxis={'title': f'{xaxis_name}'},
                                    yaxis={'title': f'{yaxis_name}'},
                                    title={'text': f'{plot_title}',
                                           'y': 0.9,
                                           'x': 0.5,
                                           'xanchor': 'center',
                                           'yanchor': 'top'}
                                    )
            },
        )


def bar_chart_page_quantity_comparison(df1, df2, df3):
    if len(df1) > 0 and len(df2) > 0:
        return html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(children=[
                            html.H5(children='Сравнение количества страниц на сайте и в поисковых системах',
                                    className="card-title"),
                            html.Div(dcc.Graph(
                                figure={'data': [
                                    {'x': df1['data_source'].tail(1),
                                     'y': df1['value'].tail(1),
                                     'type': 'bar',
                                     'name': 'Sitemap',
                                     'marker': {"color": '#27d67e'}},

                                    {'x': df2['data_source'].tail(1),
                                     'y': df2['value'].tail(1),
                                     'type': 'bar',
                                     'name': 'Yandex',
                                     'marker': {"color": '#d62728'}},

                                    {'x': df3['data_source'].tail(1),
                                     'y': df3['value'].tail(1),
                                     'type': 'bar',
                                     'name': 'Google',
                                     'marker': {"color": '#2470dc'}},
                                ],
                                    'layout': {
                                        'title': 'Сравнение количества страниц на сайте и в поисковых системах',
                                        'yaxis': {
                                            'title': 'Количество страниц',
                                        },

                                    }
                                }

                            )

                            )

                        ], className="card-body"
                        ),
                    ], className="card info-card customers-card"

                ),
            ], className="col-xxl-6 col-xl-12")
    else:
        pass


def traffic_category_bar_chart(df):
    if len(df) > 1:

        df = df.pivot_table(index=['month_year'], columns='traffic_category', values='value', sort=False)
        fig = px.bar(df, labels=dict(month_year="Период", value="Количество визитов", traffic_category="Тип страницы"))

        # fig.update_traces(marker_line_width=0, selector=dict(type='bar'))
        fig.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)'})

        return html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(
                            children=[
                                html.H5(children='Распределение трафика', className="card-title"),
                                html.Div(children=[
                                    html.Div(dcc.Graph(figure=fig))
                                ],
                                )
                            ], className="card-body"
                        )
                    ], className="card info-card customers-card"
                ),
            ], className="col-xxl-6 col-xl-12")
    else:
        pass



def update_layout(project, dashboard):

    seo_traffic_categories_data = connection.execute(
        db.select([traffic_categories_data_table])
        .where(traffic_categories_data_table.columns.project_name == project.name)
    ).fetchall()

    seo_traffic_categories_df = traffic_category_plot_database_to_df(seo_traffic_categories_data)

    df = get_seo_data(project)

    yandex_indexed_pages_quantity_df = create_slice(df, 'Yandex', 'Yandex_indexed_pages_quantity')
    google_indexed_pages_quantity_df = create_slice(df, 'Google', 'Google_indexed_pages_quantity')

    sitemap_pages_quantity_df = create_slice(df, 'Sitemap', 'Pages_quantity_in_sitemap')

    yandex_positions_df = create_slice(df, 'Yandex', 'Positions_percentage')
    google_positions_df = create_slice(df, 'Google', 'Google_positions_report')

    yandex_traffic_df = create_slice(df, 'Yandex', 'Traffic')
    google_traffic_df = create_slice(df, 'Google', 'Traffic')


    ### DASHBOARD FRONT
    dashboard.layout = html.Div(children=[

        html.Div(children=[
            html.H1(children=f"Данные по SEO {project.name}")], className="pagetitle"),

        html.Div(children=[html.H5(children="Индексирование")], className="card-title"),

        line_plot(yandex_indexed_pages_quantity_df,
                  'Количество страниц в базе Яндекса',
                  'yandex_indexed_pages_quantity_selector',
                  'yandex_indexed_pages_quantity_line_plot'),

        line_plot(google_indexed_pages_quantity_df,
                  'Количество страниц в базе Google',
                  'google_indexed_pages_quantity_selector',
                  'google_indexed_pages_quantity_line_plot'),

        bar_chart_page_quantity_comparison(sitemap_pages_quantity_df,
                                           yandex_indexed_pages_quantity_df,
                                           google_indexed_pages_quantity_df),

        html.Div(children=[html.H5(children="Позиции в поисковых системах")], className="card-title"),

        line_plot(yandex_positions_df,
                  'Доля запросов в ТОП10 Яндекса',
                  'yandex_positions_selector',
                  'yandex_positions_line_plot'),

        line_plot(google_positions_df,
                  'Доля запросов в ТОП10 Google',
                  'google_positions_selector',
                  'google_positions_line_plot'),

        html.Div(children=[html.H5(children="Трафик")], className="card-title"),

        line_plot(yandex_traffic_df,
                  'Количество визитов из Яндекса',
                  'yandex_traffic_selector',
                  'yandex_traffic_line_plot'),

        line_plot(google_traffic_df,
                  'Количество визитов из Google',
                  'google_traffic_selector',
                  'google_traffic_line_plot'),

        traffic_category_bar_chart(seo_traffic_categories_df),

    ], className="row", style={"color": "#444444"})

    # INDEXED PAGES QUANTITY
    ### Yandex
    line_plot_settings(
        dashboard=dashboard,
        output='yandex_indexed_pages_quantity_line_plot',
        input_selector='yandex_indexed_pages_quantity_selector',
        df=yandex_indexed_pages_quantity_df,
        colour='#d62728',
        xaxis_name='Дата',
        yaxis_name='Количество страниц',
        plot_title='Количество страниц в базе Яндекса'
    )

    ### Google

    line_plot_settings(
        dashboard=dashboard,
        output='google_indexed_pages_quantity_line_plot',
        df=google_indexed_pages_quantity_df,
        input_selector='google_indexed_pages_quantity_selector',
        colour='#2470dc',
        xaxis_name='Дата',
        yaxis_name='Количество страниц',
        plot_title='Количество страниц в базе Google'
    )

    # SE POSITIONS
    ### Yandex
    line_plot_settings(
        dashboard=dashboard,
        df=yandex_positions_df,
        output='yandex_positions_line_plot',
        input_selector='yandex_positions_selector',
        colour='#d62728',
        xaxis_name='Дата',
        yaxis_name='% запросов в ТОП10',
        plot_title='Доля запросов в ТОП10 Яндекса'
    )

    ### Google
    line_plot_settings(
        dashboard=dashboard,
        df=google_positions_df,
        output='google_positions_line_plot',
        input_selector='google_positions_selector',
        colour='#2470dc',
        xaxis_name='Дата',
        yaxis_name='% запросов в ТОП10',
        plot_title='Доля запросов в ТОП10 Google'
    )

    # SE TRAFFIC
    ### Yandex
    line_plot_settings(
        dashboard=dashboard,
        df=yandex_traffic_df,
        output='yandex_traffic_line_plot',
        input_selector='yandex_traffic_selector',
        colour='#d62728',
        xaxis_name='Дата',
        yaxis_name='Количество визитов',
        plot_title='Количество визитов из Яндекса'
    )

    ### Google
    line_plot_settings(
        dashboard=dashboard,
        df=google_traffic_df,
        output='google_traffic_line_plot',
        input_selector='google_traffic_selector',
        colour='#2470dc',
        xaxis_name='Дата',
        yaxis_name='Количество визитов',
        plot_title='Количество визитов из Google'
    )
