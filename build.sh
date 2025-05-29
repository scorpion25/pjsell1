#!/usr/bin/env bash

# Instala as dependências do projeto
pip install -r requirements.txt

# Aplica as migrações
python manage.py migrate --noinput

echo "👤 Criando superusuário..."

python manage.py shell << EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', '121181')
EOF
