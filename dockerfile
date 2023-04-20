# start by pulling the python image
FROM python:3.10-alpine


# COPY ./requirements.txt /app/requirements.txt
WORKDIR /app
# APP PART
# RUN pip install -r requirements.txt
RUN pip install Flask 
RUN pip install sqlalchemy
COPY ./src /app

# CRON PART
ADD ./src/crontab /etc/cron.d/crontab
RUN chmod 0644 /etc/cron.d/crontab
RUN touch /var/log/cron.log
RUN apt-get update
RUN apt-get -y install cron


# Run the command on container startup
CMD cron && tail -f /var/log/cron.log && python3 -m flask run --host=0.0.0.0

# configure the container to run in an executed manner
# CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]