#!/usr/bin/env bash

# Instala as dependências do projeto
pip install -r requirements.txt

# Aplica as migrações
python manage.py migrate --noinput
