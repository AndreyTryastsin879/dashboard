import dash
# import sqlalchemy as db

from dashapp.plot_settings import *

from app_config import Configuration

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


def create_dashboard(flask_app, project):
    print('CREATE DASHBOARD')

    dashboard = dash.Dash(
        server=flask_app,
        name='SEO Dashboard',
        url_base_pathname=f'/dash/{project}/service/seo/',
        suppress_callback_exceptions=True,
        external_stylesheets=EXTERNAL_STYLESHEET
    )

    dashboard.layout = html.Div()

    # CALLBACKS
    # Idexed_pages_quantity
    ###Yandex
    line_plot_settings(
        project=project,
        data_source='Yandex',
        df_slice_name='Yandex_indexed_pages_quantity',
        dashboard=dashboard,
        output='yandex_indexed_pages_quantity_line_plot',
        input_selector='yandex_indexed_pages_quantity_selector',
        colour='#d62728',
        xaxis_name='Дата',
        yaxis_name='Количество страниц',
        plot_title='Количество страниц в базе Яндекса'
    )

    ### Google
    line_plot_settings(project=project,
                       data_source='Google',
                       df_slice_name='Google_indexed_pages_quantity',
                       dashboard=dashboard,
                       output='google_indexed_pages_quantity_line_plot',
                       input_selector='google_indexed_pages_quantity_selector',
                       colour='#2470dc',
                       xaxis_name='Дата',
                       yaxis_name='Количество страниц',
                       plot_title='Количество страниц в базе Google'
                       )

    # # # SE POSITIONS
    # # ### Yandex
    line_plot_settings(
        project=project,
        data_source='Yandex',
        df_slice_name='Positions_percentage',
        dashboard=dashboard,
        output='yandex_positions_line_plot',
        input_selector='yandex_positions_selector',
        colour='#d62728',
        xaxis_name='Дата',
        yaxis_name='% запросов в ТОП10',
        plot_title='Доля запросов в ТОП10 Яндекса'
    )

    # # ### Google
    line_plot_settings(
        project=project,
        data_source='Google',
        df_slice_name='Google_positions_report',
        dashboard=dashboard,
        output='google_positions_line_plot',
        input_selector='google_positions_selector',
        colour='#2470dc',
        xaxis_name='Дата',
        yaxis_name='% запросов в ТОП10',
        plot_title='Доля запросов в ТОП10 Google'
    )

    # # SE TRAFFIC
    # ### Yandex
    line_plot_settings(
        project=project,
        data_source='Yandex',
        df_slice_name='Traffic',
        dashboard=dashboard,
        output='yandex_traffic_line_plot',
        input_selector='yandex_traffic_selector',
        colour='#d62728',
        xaxis_name='Дата',
        yaxis_name='Количество визитов',
        plot_title='Количество визитов из Яндекса'
    )

    # ### Google
    line_plot_settings(
        project=project,
        data_source='Google',
        df_slice_name='Traffic',
        dashboard=dashboard,
        output='google_traffic_line_plot',
        input_selector='google_traffic_selector',
        colour='#2470dc',
        xaxis_name='Дата',
        yaxis_name='Количество визитов',
        plot_title='Количество визитов из Google'
    )

    return dashboard


def update_layout(project):
    engine = db.create_engine(Configuration.SQLALCHEMY_DATABASE_URI)
    connection = engine.connect()
    metadata = db.MetaData()

    line_plots_data_table = select_table_from_db('seo_data_for_linear_plots', metadata, engine)

    traffic_categories_data_table = select_table_from_db('seo_traffic_categories', metadata, engine)

    line_plots_seo_data = slice_table_by_project_name(line_plots_data_table, project, connection)

    df = linear_plot_database_to_df(line_plots_seo_data)

    seo_traffic_categories_data = slice_table_by_project_name(traffic_categories_data_table, project, connection)

    seo_traffic_categories_df = traffic_category_plot_database_to_df(seo_traffic_categories_data)

    yandex_indexed_pages_quantity_df = create_slice(df, 'Yandex', 'Yandex_indexed_pages_quantity')
    google_indexed_pages_quantity_df = create_slice(df, 'Google', 'Google_indexed_pages_quantity')

    sitemap_pages_quantity_df = create_slice(df, 'Sitemap', 'Pages_quantity_in_sitemap')

    yandex_positions_df = create_slice(df, 'Yandex', 'Positions_percentage')
    google_positions_df = create_slice(df, 'Google', 'Google_positions_report')

    yandex_traffic_df = create_slice(df, 'Yandex', 'Traffic')
    google_traffic_df = create_slice(df, 'Google', 'Traffic')

    print(yandex_traffic_df['created'].min(), yandex_traffic_df['created'].max())

    ### DASHBOARD FRONT
    return html.Div(children=[

        html.Div(children=[
            html.H1(children=f"Данные по SEO {project.title()}")], className="pagetitle"),

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


def update_layout_callback_factory(project):
    def inner():
        return update_layout(project)

    return inner
