FROM python:3.11

# assumes app.py contains your flask app
#COPY rest_employees.py app.py
#ADD templates /templates


#New
ADD templates /var/rest-api-employee/templates
COPY rest_employees.py /var/rest-api-employee/app.py
WORKDIR /var/rest-api-employee

# install flask and gunicorn
RUN pip install flask gunicorn flask-cors

# this configuration is needed for your app to work, do not change it
ENTRYPOINT ["gunicorn", "app:app", "run", "--bind", "0.0.0.0:80"]

EXPOSE 80