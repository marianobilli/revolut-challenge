FROM python:3.9.7-slim

#-- Install requirements
# RUN apk --update add --no-cache python3-dev gcc libc-dev g++ musl-dev # these are for alpine

#-- App Setup --
RUN mkdir /opt/revolut
WORKDIR /opt/revolut
COPY app/requirements.txt .
COPY app/* .

# -- Pip requirements
RUN python3 -m pip install --no-cache-dir -r requirements.txt

#-- Flask Setup --
ENV FLASK_APP='/opt/revolut/api.py'
ENV FLASK_ENV='production' 
ENV FLASK_RUN_PORT='9000'
ENTRYPOINT ["flask", "run", "--host=0.0.0.0", "--cert=adhoc"]