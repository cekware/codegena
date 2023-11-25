# base image
FROM python:3.12.0-alpine3.17

# set working directory
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# add requirements (to leverage Docker cache)
ADD ./requirements.txt /usr/src/app/requirements.txt

# RUN pip install --upgrade pip
RUN apk add gcc musl-dev libffi-dev
# install requirements
RUN pip install -r requirements.txt


# copy project
COPY . /usr/src/app
