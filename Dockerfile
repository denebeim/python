FROM python:slim

RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY src /src
WORKDIR /src

RUN python manage.py collectstatic

# wasting too much time on this, just create the db by hand and run as root
# RUN addgroup --system nonroot && adduser --system --group nonroot
# RUN python manage.py migrate
# RUN chown nonroot db.sqlite3

# USER nonroot

ENV DJANGO_DEBUG_FALSE=1
CMD gunicorn --bind :8888 superlists.wsgi:application
# CMD python manage.py runserver 0.0.0.0:8888
