import json

import requests

# url = "18.219.48.122:9494/extractTables"
csvToQueryURL = "http://3.136.158.249:9300/QueryCSV"
headers = {}


def post_call(message):
    payload = {'query': message}
    files = [
        ('file', ('prediction_report.csv', open('C:/Users/gopasali/PycharmProjects/PyExcersice/prediction'
                                                '/prediction_output/prediction_report.csv', 'rb')))]

    try:
        response = requests.request("POST", csvToQueryURL, headers=headers, data=payload, files=files)
        print('Response is', response.text)
        data = json.loads(response.text)

        if not data['answer']:
            return 'No records found!!'
        else:
            return ', '.join([str(x) for x in data['answer']])
    except Exception as ex:
        print('Failed to fetch data from RESTFUL service!!!')
        print(str(ex))
        return 'Invalid input or Failed to fetch data from RESTFUL service'


if __name__ == "__main__":
    print(post_call("what is the inventory?"))
