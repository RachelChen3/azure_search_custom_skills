# To enable ssh & remote debugging on app service change the base image to the one below
# FROM mcr.microsoft.com/azure-functions/python:2.0-python3.6-appservice
FROM mcr.microsoft.com/azure-functions/python:2.0-python3.6

ENV AzureWebJobsScriptRoot=/home/site/wwwroot \
    AzureFunctionsJobHost__Logging__Console__IsEnabled=true

COPY requirements.txt /
RUN apt-get update
RUN apt-get -y install git
RUN pip install --upgrade pip
RUN pip install -r /requirements.txt
RUN pip install git+https://github.com/LIAAD/yake

COPY . /home/site/wwwroot