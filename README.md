# Azure Cognitive Search pipeline based on a custom container 

This tutorial explains how to build an Azure Cognitive Search enrichment pipeline based on a custom container. We build a search to extract ducth keywords and return the scores. 

## Steps: 
- Buid a docker container that extract ducth keywords by YAKE library.
- Build Azure function based on the docker container
- Build a custome skill based on this Azure function 
- Buiild a search index based on this skill.

Note: you need to change the <your storage connection string> in the following files:
  - LocalFunctionsProject/local.settings.json
  - step.sh


[Tutorial](https://medium.com/@rachel_95942/create-an-azure-cognitive-search-pipeline-based-on-a-custom-container-python-1bc757e69659) is avaliable. 

