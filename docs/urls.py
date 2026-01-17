from django.urls import path
from . import views

urlpatterns = [
    path('', views.contents, name='docs-contents'),
    path('django/project-intro', views.project_intro, name='project-intro'),
    path('django/setup', views.django_setup, name='django-setup'),
    path('django/orm', views.django_orm, name='django-orm'),
    path('django/model', views.django_model, name='django-model'),
    path('django/regexp', views.django_regexp, name='django-regexp'),
    path('django/datetime', views.django_datetime, name='django-datetime'),
    path('django/django-tips', views.django_django_tips, name='django-tips'),

    path('psql/note', views.psql_note, name='docs-psql-note'),
    path('psql/datatype', views.psql_datatype, name='docs-psql-datatype'),
    path('psql/crud', views.psql_crud, name='docs-psql-crud'),
    path('psql/select', views.psql_select, name='docs-psql-select'),
    path('psql/constraints', views.psql_constraints, name='docs-psql-constraints'),
    path('psql/groupby', views.psql_groupby, name='docs-psql-groupby'),
    path('psql/join', views.psql_join, name='docs-psql-join'),
    path('psql/aggregate', views.psql_aggregate, name='docs-psql-aggregate'),
    path('psql/functions', views.psql_functions, name='docs-psql-functions'),
    path('psql/procedure-trigger', views.psql_procedure_trigger, name='docs-psql-procedure-trigger'),

    path('flask/install', views.flask_install, name='docs-flask-install'),
    path('flask/note', views.flask_note, name='docs-flask-note'),
    path('flask/core-crud', views.flask_core_crud, name='docs-flask-core-crud'),
    path('flask/db-setup', views.flask_db_setup, name='docs-flask-db-setup'),
    path('flask/sqlalchemy', views.flask_sqlalchemy, name='docs-flask-sqlalchemy'),

    path('python/datatype', views.python_datatype, name='docs-python-datatype'),
    path('python/print-format', views.python_print_format, name='docs-python-print-format'),
    path('python/loop', views.python_loop, name='docs-python-loop'),
    path('python/def-file', views.python_def_file, name='docs-python-def-file'),
    path('python/class-module', views.python_class_module, name='docs-python-class-module'),
    path('python/try-except', views.python_try_except, name='docs-python-try-except'),
    path('python/py-library', views.python_py_library, name='docs-python-py-library'),
    path('python/decorator', views.python_decorator, name='docs-python-decorator'),
    path('python/regexp', views.python_regexp, name='docs-python-regexp'),

    path('others/linux', views.linux, name='docs-linux'),
    path('others/basic-settings', views.basic_settings, name='docs-basic-settings'),
    path('others/html-css', views.html_css, name='docs-html-css'),
]