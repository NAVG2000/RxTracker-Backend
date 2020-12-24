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
ARG AWS_ACCESS_KEY_ID
ARG AWS_SECRET_ACCESS_KEY
ENV aws_access_key_id = $AWS_ACCESS_KEY_ID
ENV aws_secret_access_key = $AWS_SECRET_ACCESS_KEY
RUN mkdir ~/.aws && touch ~/.aws/credentials && printf "[default]\naws_access_key_id = $aws_access_key_id\naws_secret_access_key = $aws_secret_access_key" >> ~/.aws/credentials
RUN touch touch ~/.aws/config && printf "[default]\nregion=us-east-1" >> ~/.aws/config
RUN python tests.py -f
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "rxtracker-api:app"]