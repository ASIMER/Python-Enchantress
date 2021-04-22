FROM python

RUN pip install django

COPY ./django_site/my_site /app
WORKDIR /app

RUN ls -la

EXPOSE 8000

CMD python manage.py runserver 0:8000
