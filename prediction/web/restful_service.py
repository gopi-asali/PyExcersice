import requests

# url = "18.219.48.122:9494/extractTables"

url = "3.136.158.249:9300/QueryCSV"
files = [
    ('file', ('prediction_report.csv', open('C:/Users/gopasali/PycharmProjects/PyExcersice/prediction'
                                            '/prediction_output/prediction_report.csv', 'rb'),
              'application/vnd.ms-excel'))
]
headers = {'accept': 'application/json',
           'Content-Type': 'multipart/form-data'
           }


def post_call(message):
    payload = {message}
    try:
        response = requests.request("POST", url, headers=headers, data=payload, files=files)
        print(response.text)
        return response.text
    except:
        return "REST Service is under construction! Try after sometime"
