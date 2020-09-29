# Deploying Converter (API) on AWS as a Lambda function

## Overview
New converter python code deployed with Flask on AWS or locally

### Prep python environment
Create a virtual environment
```
cd deploy-aws
virtualenv venv
source ./venv/bin/activate
```

Install modules including zappa, Flask
```pip3 install -r requirements.txt```

Initialize zappa and configure auth to AWS
TODO

Deploy to AWS
```zappa update dev```     (if not yet deployed zappa deploy dev)

To re(certify) the ACM SSL cert created
```zappa certify```

Watching the logs
```zappa tail```