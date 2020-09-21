# Data-Converter
An api that accepts a deal in one format and returns another

### Intended Formats
- JSON
- PBN
- UUID
- ...

There are two services
* A containerised function on GCP
* A cloud function on AWS (Lambda via API Gateway)

## Usage - containerised function on GCP
### when the SSL cert is fixed
```
curl --insecure -F "file=@src/test.pbn" https://converter.prod.globalbridge.app/api/boards/test
```
### when the SSL cert is broken
```
curl --insecure -F "file=@src/test.pbn" https://converter.prod.globalbridge.app/api/boards/test
```

## Usage - cloud function on AWS
Output choices: human, pbn, rbn, lin
Function file is [bridgeDealConverter-api.py](https://github.com/online-bridge-hackathon/Data-Converter/tree/master/bridgeDealConverter)
```
curl --header "Content-Type: application/json" --request POST --data '{"uuid":"0x63b40b7f2842298cb3bea48", "output":"pbn"}' https://pur12pbdu8.execute-api.eu-west-2.amazonaws.com/deal
```
