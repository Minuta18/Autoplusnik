# Autoplusnik Copyright (C) 2023 Igor Samsonov

import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SECRET_KEY = '''LZ4kUsKvQHFmxXhJ+4ZmQb/JI542yZNbiSqudGgzM50ipGAB5HqDysMNQnEif559H2mnfmy0foWrm49jsnQUKA=='''