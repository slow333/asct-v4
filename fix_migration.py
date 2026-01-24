#!/usr/bin/env python
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.db import connection

cursor = connection.cursor()
cursor.execute("DELETE FROM django_migrations WHERE app='socialaccount'")
cursor.execute("DELETE FROM django_migrations WHERE app='sites'")
cursor.execute("DELETE FROM django_migrations WHERE app='account'")
print('마이그레이션 기록 삭제 완료')
