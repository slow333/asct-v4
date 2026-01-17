from django.shortcuts import render
from django.http import HttpResponse

def contents(requst):
    return render(requst, 'docs/contents.html')


# ============= django ========================
def django_django_tips(requst):
    return render(requst, 'docs/django/django-tips.html')

def project_intro(requst):
    return render(requst, 'docs/django/project-intro.html')

def django_setup(requst):
    return render(requst, 'docs/django/setup.html')

def django_orm(requst):
    return render(requst, 'docs/django/django-orm.html')

def django_model(requst):
    return render(requst, 'docs/django/about-models.html')

def django_regexp(requst):
    return render(requst, 'docs/django/regexp.html')

def django_datetime(requst):
    return render(requst, 'docs/django/datetime.html')

# ============= flask ========================
def flask_install(requst):
    return render(requst, 'docs/flask/install.html')

def flask_note(requst):
    return render(requst, 'docs/flask/note.html')

def flask_core_crud(requst):
    return render(requst, 'docs/flask/core_crud.html')

def flask_db_setup(requst):
    return render(requst, 'docs/flask/db_setup.html')

def flask_sqlalchemy(requst):   
    return render(requst, 'docs/flask/sqlalchemy.html')

# ============= postgresql database ========================
def psql_note(requst):
    return render(requst, 'docs/postgresql/00-psql-note.html')

def psql_index(requst):
    return render(requst, 'docs/postgresql/00-database-index.html')

def psql_datatype(requst):
    return render(requst, 'docs/postgresql/01-datatype.html')


def psql_crud(requst):
    return render(requst, 'docs/postgresql/02-crud.html')


def psql_select(requst):   
    return render(requst, 'docs/postgresql/03-select.html')

def psql_constraints(requst):   
    return render(requst, 'docs/postgresql/04-constraints.html')

def psql_groupby(requst):   
    return render(requst, 'docs/postgresql/05-groupby.html')

def psql_join(requst):   
    return render(requst, 'docs/postgresql/06-join.html')

def psql_aggregate(requst):   
    return render(requst, 'docs/postgresql/07-aggregate.html')

def psql_functions(requst):   
    return render(requst, 'docs/postgresql/08-functions.html')

def psql_procedure_trigger(requst):
    return render(requst, 'docs/postgresql/09-procedure-trigger.html')


# ============= python ========================

def python_datatype(requst):   
    return render(requst, 'docs/python/01_datatype.html')

def python_print_format(requst):   
    return render(requst, 'docs/python/02_print_format.html')

def python_loop(requst):   
    return render(requst, 'docs/python/03_loop.html')

def python_def_file(requst):   
    return render(requst, 'docs/python/04_def_file.html')

def python_class_module(requst):   
    return render(requst, 'docs/python/05_class_module.html')

def python_try_except(requst):   
    return render(requst, 'docs/python/06_try_except.html')

def python_py_library(requst):   
    return render(requst, 'docs/python/07_py_library.html')

def python_decorator(requst):   
    return render(requst, 'docs/python/08_closer_decorator.html')

def python_regexp(requst):   
    return render(requst, 'docs/python/09_regexp.html')


# ============= others ========================

def linux(requst):   
    return render(requst, 'docs/others/linux.html')

def basic_settings(requst):   
    return render(requst, 'docs/others/basic-settings.html')

def html_css(requst):
    return render(requst, 'docs/others/html_css.html')