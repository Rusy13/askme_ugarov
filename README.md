Для запуска проекта:
1) python -m venv venv - создайте виртуальное окружение с помощью встроенного модуля venv
2) source venv/bin/activate - активируйте виртуальное окружение(Linux и macOS) В Windows:venv\Scripts\activate
3) pip install -r requirements.txt - установите зависимости
4) python manage.py runserver - запустите сервер
5) Откройте браузер и перейдите по адресу http://127.0.0.1:8000/ (далее выберите путь)


6) Прогоните миграции - 
python manage.py makemigrations
python manage.py migrate
7) Заполните базу - python manage.py fill_db [ratio]

Запуск с Gunicorn:
gunicorn -w 2 technop.wsgi:simple_app -b localhost:8081

# Пример GET запроса
curl "http://localhost:8081?param1=value1&param2=value2"
# Пример POST запроса
curl -X POST -d "param1=value1&param2=value2" http://localhost:8081



Можно зайти через nginx: http://localhost

