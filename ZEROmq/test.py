import requests

def get_ipadrress():
    url = "https://api.ipify.org?format=json"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data["ip"]
        else:
            return "Failed to retrieve public IP"
    except requests.RequestException:
        return "Failed to retrieve public IP"

