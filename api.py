import sys
import os
import shutil
import time
import traceback
from loguru import logger

from flask import Flask, request, jsonify
import pandas as pd
from sklearn.externals import joblib
from sklearn.ensemble import RandomForestClassifier as rf


app = Flask(__name__)

TRAINING_DATA = os.path.join(os.path.dirname(__file__), "data", "titanic.csv")

if not os.path.isfile(TRAINING_DATA):
    raise FileNotFoundError("please check the input directory and file")

INCLUDES = ["Age", "Sex", "Embarked", "Survived"]

DEPENDENT_VARIABLE = "Survived"

MODEL_DIRECTORY = os.path.join(os.path.dirname(__file__), "model")
MODEL_FILE_NAME = os.path.join(MODEL_DIRECTORY, "model.pkl")
MODEL_COLUMN_FILE_NAME = os.path.join(MODEL_DIRECTORY, "model_columns.pkl")

model_columns = None
clf = None


@app.route("/predict", methods=["POST"])
def predict():
    if clf:
        try:
            json_ = request.json
            query = pd.get_dummies(pd.DataFrame(json_))
            query = query.reindex(columns=model_columns, fill_value=0)

            prediction = list(clf.predict(query))

            return jsonify({"prediction": [int(x) for x in prediction]})

        except Exception as e:
            return jsonify({"error": str(e), "trace": traceback.format_exc()})
    else:
        logger.info("Train the classifier first")

        return "No Model Found"


@app.route("/train", methods=["GET"])
def train():
    df = pd.read_csv(TRAINING_DATA)
    df_ = df[INCLUDES]

    categoricals = []

    for col, col_type in df_.dtypes.iteritems():
        if col_type == "0":
            categoricals.append(col)
        else:
            df_[col].fillna(0, inplace=True)

    df_one_hot_encode = pd.get_dummies(df_, columns=categoricals, dummy_na=True)
    X = df_one_hot_encode[df_one_hot_encode.columns.difference(DEPENDENT_VARIABLE)]
    y = df_one_hot_encode[DEPENDENT_VARIABLE]

    global model_columns
    model_columns = list(x.columns)
    joblib.dump(model_columns, MODEL_COLUMN_FILE_NAME)

    global clf
    clf = rf()
    start = time.time()
    clf.fit(X, y)
    logger.info(f"Trained in {time.time() - start} seconds")
    logger.info(f"Model Training score {clf.score(X, y)}")

    joblib.dump(clf, MODEL_FILE_NAME)

    return "SUCCESS"


@app.route("/wipe", methods=["GET"])
def wipe():
    try:
        shutil.rmtree("model")
        os.makedirs(MODEL_DIRECTORY)
        return "Model Wiped"
    except Exception as e:
        print(str(e))
        return "Could not remove and recreate the model directory"


if __name__ == "__main__":
    try:
        PORT = int(sys.argv[1])
    except Exception as e:
        PORT = 80

    try:
        clf = joblib.load(MODEL_FILE_NAME)
        logger.info("Model Loaded")
        model_columns = joblib.load(MODEL_COLUMN_FILE_NAME)
        logger.info("Model Columns Loaded")
    except Exception as e:
        logger.info("No Model Here")
        logger.info("Train the Model First")
        logger.info(str(e))
        clf = None

    app.run(host="0.0.0.0", port=PORT, debug=False)
