from datetime import datetime, timedelta

from dash import html
from dash import dcc

from dash.dependencies import Input, Output

import plotly.graph_objs as go
import plotly.express as px


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
                                children=f'Доступны данные за период {start_date.strftime("%d %B %Y")} - {end_date.strftime("%d %B %Y")}'),

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