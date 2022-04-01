from app import db
from datetime import datetime
from flask_security import UserMixin, RoleMixin


projects_services = db.Table(
    'projects_services',
    db.Column('project_id', db.Integer, db.ForeignKey('project.id')),
    db.Column('service_id', db.Integer, db.ForeignKey('service.id'))
)

projects_notes = db.Table(
    'projects_notes',
    db.Column('project_id', db.Integer, db.ForeignKey('project.id')),
    db.Column('note_id', db.Integer, db.ForeignKey('note.id'))
)

roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'))
)


class Project(db.Model):
    def __init__(self, *args, **kwargs):
        super(Project, self).__init__(*args, **kwargs)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300))
    slug = db.Column(db.String(300), unique=True)
    domain = db.Column(db.String(300))
    yandex_metrika_counter_id = db.Column(db.Integer)
    yandex_webmaster_host = db.Column(db.String(300))
    seranking_id = db.Column(db.Integer)
    sitemap_path = db.Column(db.String(300))
    second_sitemap_path = db.Column(db.String(300))
    created = db.Column(db.DateTime, default=datetime.now())

    services = db.relationship('Service', secondary=projects_services, backref=db.backref('projects', lazy='dynamic'))
    notes = db.relationship('Note', secondary=projects_notes, backref=db.backref('projects', lazy='dynamic'))

    def __repr__(self):
        return 'Project id: {}, name: {}'.format(self.id, self.name)


class Seo_data_for_linear_plots(db.Model):
    def __init__(self, *args, **kwargs):
        super(Seo_data_for_linear_plots, self).__init__(*args, **kwargs)

    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(300))
    data_source = db.Column(db.String(300))
    data_type = db.Column(db.String(300))
    value = db.Column(db.Integer)
    created = db.Column(db.DateTime)


class Seo_traffic_categories(db.Model):
    def __init__(self, *args, **kwargs):
        super(Seo_traffic_categories, self).__init__(*args, **kwargs)

    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(300))
    traffic_category = db.Column(db.String(300))
    value = db.Column(db.Integer)
    month_year = db.Column(db.String(300))
    created = db.Column(db.DateTime)


class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300))
    slug = db.Column(db.String(300))

    def __init__(self, *args, **kwargs):
        super(Service, self).__init__(*args, **kwargs)

    def __repr__(self):
        return '{}'.format(self.name)


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300))
    period = db.Column(db.String(300))
    text = db.Column(db.Text)
    created = db.Column(db.DateTime)

    def __init__(self, *args, **kwargs):
        super(Note, self).__init__(*args, **kwargs)

    def __repr__(self):
        return '{} {}'.format(self.title, self.period)


class Data_collecting_report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(300))
    report_name = db.Column(db.String(300))
    status = db.Column(db.String(300))
    value = db.Column(db.String(300))
    error_text = db.Column(db.Text)
    created = db.Column(db.DateTime)

    def __init__(self, *args, **kwargs):
        super(Data_collecting_report, self).__init__(*args, **kwargs)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(200))
    active = db.Column(db.Boolean())
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(250))