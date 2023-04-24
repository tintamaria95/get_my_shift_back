# start by pulling the python image
FROM python:3.10-alpine


# COPY ./requirements.txt /app/requirements.txt
WORKDIR /app
# APP PART
# RUN pip install -r requirements.txt
RUN pip install Flask 
RUN pip install sqlalchemy
COPY ./src /app

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]