import urllib.request
import urllib.error
import json

api_key = 'AQ.Ab8RN6IHjduHiO63woLFpTNZTpkASp9jkHBVdegEMo3-GNQ0zg'
url = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash:streamGenerateContent?alt=sse&key={api_key}'

prompt = "A" * 7000

payload = {
    "system_instruction": {
        "parts": [{"text": "Bạn là một chuyên gia dịch thuật."}]
    },
    "contents": [{"role": "user", "parts": [{"text": prompt}]}]
}
data = json.dumps(payload).encode('utf-8')
req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})

try:
    urllib.request.urlopen(req)
    print("Success")
except urllib.error.HTTPError as e:
    print(f'Status: {e.code}')
    print(f'Body: {e.read().decode()}')
