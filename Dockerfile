FROM python:latest
RUN mkdir /code
COPY requirements.txt /code
RUN pip install -r /code/requirements.txt
COPY . /code
WORKDIR /code
CMD bash -c "python3 manage.py collectstatic --no-input && gunicorn api_yamdb.wsgi:application --bind 0.0.0.0:8000"
