from app import app
from flask import render_template

from models import Project, Service, Data_collecting_report

from dashapp.seo_dashboard_app import update_layout_callback_factory


def select_report(slug, report_name):
    report = Data_collecting_report.query \
        .filter(Data_collecting_report.project_name == slug,
                Data_collecting_report.report_name == report_name) \
        .order_by(Data_collecting_report.id.desc()).first()
    return report


@app.route('/')
def index():
    projects = Project.query.all()
    return render_template('index.html', projects=projects)


@app.route('/<slug>/')
def project_detail(slug):
    projects = Project.query.all()
    project = Project.query.filter(Project.slug == slug).first_or_404()
    notes = project.notes
    yandex_traffic_report = select_report(slug, 'Yandex_traffic_metrika_report')
    google_traffic_report = select_report(slug, 'Google_traffic_metrika_report')
    yandex_positions_report = select_report(slug, 'Yandex_positions_report')
    google_positions_report = select_report(slug, 'Google_positions_report')
    yandex_indexed_pages_quantity_report = select_report(slug, 'Yandex_indexed_pages_quantity')
    google_indexed_pages_quantity_report = select_report(slug, 'Google_indexed_pages_quantity')
    pages_quantity_in_sitemap_report = select_report(slug, 'Pages_quantity_in_sitemap')
    traffic_categories_report = select_report(slug, 'Traffic_categories_report')
    return render_template('project_detail.html',
                           project=project,
                           projects=projects,
                           notes=notes,
                           yandex_traffic_report=yandex_traffic_report,
                           google_traffic_report=google_traffic_report,
                           yandex_positions_report=yandex_positions_report,
                           google_positions_report=google_positions_report,
                           yandex_indexed_pages_quantity_report=yandex_indexed_pages_quantity_report,
                           google_indexed_pages_quantity_report=google_indexed_pages_quantity_report,
                           pages_quantity_in_sitemap_report=pages_quantity_in_sitemap_report,
                           traffic_categories_report=traffic_categories_report)


@app.route('/<slug>/error/')
def error_report(slug):
    projects = Project.query.all()
    project = Project.query.filter(Project.slug == slug).first_or_404()
    yandex_traffic_report = select_report(slug, 'Yandex_traffic_metrika_report')
    google_traffic_report = select_report(slug, 'Google_traffic_metrika_report')
    yandex_positions_report = select_report(slug, 'Yandex_positions_report')
    google_positions_report = select_report(slug, 'Google_positions_report')
    yandex_indexed_pages_quantity_report = select_report(slug, 'Yandex_indexed_pages_quantity')
    google_indexed_pages_quantity_report = select_report(slug, 'Google_indexed_pages_quantity')
    pages_quantity_in_sitemap_report = select_report(slug, 'Pages_quantity_in_sitemap')
    traffic_categories_report = select_report(slug, 'Traffic_categories_report')
    all_reports = [yandex_traffic_report,
                   google_traffic_report,
                   yandex_positions_report,
                   google_positions_report,
                   yandex_indexed_pages_quantity_report,
                   google_indexed_pages_quantity_report,
                   pages_quantity_in_sitemap_report,
                   traffic_categories_report
                   ]
    return render_template('error_report_detail.html',
                           projects=projects,
                           project=project,
                           all_reports=all_reports)


@app.route('/<project_slug>/service/<service_slug>/')
def seodashboard(project_slug, service_slug):
    projects = Project.query.all()
    current_project = Project.query.filter(Project.slug == project_slug).first()
    current_service = Service.query.filter(Service.slug == service_slug).one_or_none()
    sidebar_closed = True
    update_layout_callback_factory(current_project.name)
    return render_template('dashboard_detail.html',
                           dash_url=f'/dash/{project_slug}/service/{service_slug}',
                           projects=projects,
                           current_project=current_project,
                           current_service=current_service,
                           sidebar_closed=sidebar_closed)
