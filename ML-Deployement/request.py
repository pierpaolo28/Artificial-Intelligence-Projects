import requests

url = 'https://pierpaolo28.github.io/predict_api'
r = requests.post(url,json={'experience':2, 'test_score':9, 'interview_score':6, 'interview':7})

print(r.json())