#!bin/bash
#
#starting the api

python api.py 9999 & sleep 2


#GET method train

curl -X GET http://localhost/train && echo -e '\n train OK'

#POST predict method
curl -d '[
    
    {"Age": 85, "Sex": "male", "Embarked": "S"},
    {"Age": 24, "Sex": "female", "Embarked": "C"},
    {"Age": 3, "Sex": "male", "Embarked": "C"},
    {"Age": 21, "Sex": "male", "Embarked": "S"}
    
    ]' -H 'Content-type : application/json' -X POST http://localhost:9999/predict && echo -e '\n -> predict OK'

#GET method wipe
curl -X GET http://localhost:9999/wipe && echo -e '\n -> wipe OK'
