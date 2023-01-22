from flask import Flask, render_template, request
import random
import pandas as pd
import json
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

with open("question.json") as json_data:
    question = json.load(json_data)
    q = pd.DataFrame(question)
    x = random.randint(0, 7)
    y = x + 1

    print(x, y)
    ques = (q['questions'][x]['%s' % (y)])
    for i in range(len(q['questions'][x]['keywords'])):
        '''print(q['questions'][1]['keywords'][i])'''

    keyword = (q['questions'][x]['keywords'][i])
    keywords = keyword
    keywords = str(keywords).lower()

app = Flask(__name__)


@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html")


@app.route("/result", methods=['POST', "GET"])
def result():
    output = request.form.to_dict()
    print(output)
    name = output["name"]
    answer = name
    print("user said : ", answer)

    x_list = word_tokenize(keywords)
    print(x_list)
    y_list = word_tokenize(answer)
    print(y_list)

    sw = stopwords.words('english')
    l1 = []
    l2 = []

    X_set = {w for w in x_list if not w in sw}
    Y_set = {w for w in y_list if not w in sw}

    rvector = X_set.union(Y_set)
    for w in rvector:
        if w in X_set:
            l1.append(1)
        else:
            l1.append(0)
        if w in Y_set:
            l2.append(1)
        else:
            l2.append(0)
    c = 0

    for i in range(len(rvector)):
        c += l1[i] * l2[i]
    cosine = c / float((sum(l1) * sum(l2)) ** 0.5)
    perc1 = round(cosine, 1) * 100
    print("Answer matching percentage is:", perc1, "%")

    pc = perc1

    return render_template("index.html", name=name, qs=ques, pc=pc,  qsn=ques)


if __name__ == '__main__':
    app.run(debug=True, port=5001)
