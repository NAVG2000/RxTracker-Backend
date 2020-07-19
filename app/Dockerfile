FROM python:3.7-stretch AS base

FROM base AS builder
RUN mkdir /install
WORKDIR /install
COPY requirements.txt /requirements.txt
RUN pip install --upgrade pip
RUN pip install --trusted-host pypi.python.org -r /requirements.txt

FROM base
COPY --from=builder /usr/local /usr/local
COPY . /app
WORKDIR /app
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "rxtracker-api:app"]