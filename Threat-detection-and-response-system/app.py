# from flask import Flask, request, jsonify
# import pickle

# # Load model and vectorizer
# model = pickle.load(open("clf.pkl", "rb"))
# cv = pickle.load(open("cv.pkl", "rb"))

# app = Flask(__name__)

# @app.route('/predict', methods=['POST'])
# def predict():
#     email_text = request.json['email']
#     processed_text = clean(email_text)  # Ensure you define or import your clean function
#     features = cv.transform([processed_text])
#     prediction = model.predict(features)[0]
#     label = "Spam" if prediction == 1 else "Not Spam"
#     return jsonify({'prediction': label})

# if __name__ == '__main__':
#     app.run(debug=True)
 
import pickle
import re
from flask import Flask, jsonify, request
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

# Ensure required NLTK resources are available
nltk.download("punkt", quiet=True)
nltk.download("punkt_tab", quiet=True)
nltk.download("stopwords", quiet=True)

# Load model and vectorizer
with open("clf.pkl", "rb") as f:
    model = pickle.load(f)

with open("cv.pkl", "rb") as f:
    cv = pickle.load(f)

app = Flask(__name__)
stop_words = set(stopwords.words("english"))
ps = PorterStemmer()


def clean(txt):
    txt = re.sub(r"\W", " ", txt)
    txt = txt.lower()
    word_tokens = word_tokenize(txt)
    filtered_text = [word for word in word_tokens if word not in stop_words]
    stemmed_text = [ps.stem(word) for word in filtered_text]
    return " ".join(stemmed_text)


@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json(silent=True)
    if not data or "email" not in data:
        return jsonify({"error": "Missing 'email' field in JSON payload"}), 400

    email_text = data["email"]
    processed_text = clean(email_text)
    features = cv.transform([processed_text])
    prediction = model.predict(features)[0]

    label = "Spam" if prediction == "Spam Email" else "Not Spam"
    return jsonify({"prediction": label})


if __name__ == "__main__":
    app.run(debug=True)