import logging
import azure.functions as func
import yake
import json

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        body = json.dumps(req.get_json())
    except ValueError:
        return func.HttpResponse(
             "Invalid body",
             status_code=400
        )
    
    if body:
        result = compose_response(body)
        return func.HttpResponse(result, mimetype="application/json")
    else:
        return func.HttpResponse(
             "Invalid body",
             status_code=400
        )


def compose_response(json_data):
    values = json.loads(json_data)['values']
    
    # Prepare the Output before the loop
    results = {}
    results["values"] = []
    
    for value in values:
        output_record = transform_value(value)
        if output_record != None:
            results["values"].append(output_record)
    return json.dumps(results, ensure_ascii=False)

## Perform an operation on a record
def transform_value(value):
    try:
        recordId = value['recordId']
    except AssertionError  as error:
        return None

    # Validate the inputs
    try:         
        assert ('data' in value), "'data' field is required."
        data = value['data']        
        assert ('content' in data), "'content' field is required in 'data' object."
        # assert ('text2' in data), "'text2' field is required in 'data' object."
    except AssertionError  as error:
        return (
            {
            "recordId": recordId,
            "errors": [ { "message": "Error:" + error.args[0] }   ]       
            })

    try:
            # if text:
        language = "nl"
        max_ngram_size = 3

        deduplication_thresold = 0.9
        deduplication_algo = 'seqm'
        windowSize = 1
        numOfKeywords = 20

        custom_kw_extractor = yake.KeywordExtractor(lan=language, n=max_ngram_size, dedupLim=deduplication_thresold, dedupFunc=deduplication_algo, windowsSize=windowSize, top=numOfKeywords, features=None)
        keywords = custom_kw_extractor.extract_keywords(value['data']['content']) 

        keywords = sorted(keywords, key=lambda tup: tup[1],reverse=True)

        keyslist= [tup[0] for tup in keywords]
        valuelist = [tup[1] for tup in keywords]

        # Here you could do something more interesting with the inputs

    except:
        return (
            {
            "recordId": recordId,
            "errors": [ { "message": "Could not complete operation for record." }   ]       
            })

    return ({
            "recordId": recordId,
            "data": {
                "keywords": keyslist,
                "keywordscores":valuelist
                    }
            })


    # text = req.params.get('text')
    # ngram = req.params.get('ngram')
    # nkey = req.params.get('nkey')
    # if not text:
    #     try:
    #         req_body = req.get_json()
    #     except ValueError:
    #         pass
    #     else:
    #         text = req_body.get('text')

    # if text:
    #     language = "nl"
    #     if ngram:
    #         max_ngram_size = int(ngram)
    #     else:
    #         max_ngram_size = 3

    #     deduplication_thresold = 0.9
    #     deduplication_algo = 'seqm'
    #     windowSize = 1
    #     if nkey:
    #         numOfKeywords = int(nkey)
    #     else:
    #         numOfKeywords = 20

    #     custom_kw_extractor = yake.KeywordExtractor(lan=language, n=max_ngram_size, dedupLim=deduplication_thresold, dedupFunc=deduplication_algo, windowsSize=windowSize, top=numOfKeywords, features=None)
    #     keywords = custom_kw_extractor.extract_keywords(text)

    #     # for kw in keywords:
    #     #     print(kw)

    #     return func.HttpResponse(str(dict(keywords)))
    # else:
    #     return func.HttpResponse(
    #          "Please pass a text on the query string or in the request body",
    #          status_code=400
    #     )
