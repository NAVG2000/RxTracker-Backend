FROM python:3.6-stretch
WORKDIR /app
COPY . /app
RUN pip install --trusted-host pypi.python.org -r requirements.txt
CMD ["gunicorn", "--bind", "0.0.0.0:80", "vascepaTestApi:app"]