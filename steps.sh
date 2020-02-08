#!/usr/bin/env bash
cd LocalFunctionsProject
docker login
docker build --tag <your docker id>/azurefunctionsimage:v1.0.0 .
docker push <your docker id>/azurefunctionsimage:v1.0.1


az login
# Function app and storage account names must be unique.
storageName=mystorageaccount$RANDOM
functionAppName=myserverlessfunc$RANDOM
functionPlanName=myappfunc$RANDOM

az group create --name testsearchgroup --location westeurope

# Create an Azure storage account in the resource group.
az storage account create \
  --name $storageName \
  --location westeurope \
  --resource-group testsearchgroup \
  --sku Standard_LRS

az functionapp plan create \
--resource-group testsearchgroup \
--name $functionPlanName \
--location westeurope \
--number-of-workers 1 \
--sku EP1 \
--is-linux

az functionapp create --name $functionAppName \
--storage-account $storageName \
--resource-group testsearchgroup \
--plan $functionPlanName \
--deployment-container-image-name rachelchen0831/azurefunctionsimage:v1.0.0

# this will return your storage connection string (a long encoded string that begins with "DefaultEndpointProtocol=")
az storage account show-connection-string \
--resource-group testsearchgroup \
--name $storageName \
--query connectionString \
--output tsv


az functionapp config appsettings set --name $functionAppName \
--resource-group testsearchgroup \
--settings AzureWebJobsStorage="your storage connection string"


az functionapp config appsettings set --name $functionAppName \
--resource-group testsearchgroup \
--settings FUNCTIONS_EXTENSION_VERSION="the run time version you perfer"

## below is the commands for tweaking parameters of Yake and update the azure function
#cd HttpExample & nano __init__.py
#cd ..
#docker build --tag <your docker id>/azurefunctionsimage:"your updated version, s.t. v1.0.0" .
#docker push <your docker id>/azurefunctionsimage:"your updated version, s.t. v1.0.0"

#az functionapp config container set -n $functionAppName \
#-g testsearchgroup \

#--docker-custom-image-name rachelchen0831/azurefunctionsimage:"your updated version, s.t. v1.0.0"
