from flask import Flask, render_template, request, json
from inventory import inventory_prediction
from web import restful_service
app = Flask(__name__)
ins = inventory_prediction.inventory_prediction()
ins.predict()

@app.route("/")
def main():
    return render_template('index.html')


@app.route('/get_results', methods=['POST'])
def get_results():
    query = request.form['ques']
    print('Question posted is: ', query)

    if not query:
        data = "You forgot to fill in this form-element."
    else:
        result = restful_service.post_call(query)
        data = "Answer is: "+result

    return render_template('index.html', data=data)


if __name__ == "__main__":
    app.run()
