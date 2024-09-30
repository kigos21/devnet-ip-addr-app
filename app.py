import os
from flask import Flask, render_template
import requests

app = Flask(__name__)

# Replace with your actual API key from ipstack.com
API_KEY = os.environ.get('IPSTACK_API_KEY')

def get_ip_info():
    try:
        response = requests.get(f"http://api.ipstack.com/check?access_key={API_KEY}")
        data = response.json()
        return {
            "ipv4": data.get("ip"),
            "ipv6": data.get("ip") if data.get("type") == "ipv6" else "Not available",
            "country": data.get("country_name"),
            "region": data.get("region_name"),
            "city": data.get("city"),
            "latitude": data.get("latitude"),
            "longitude": data.get("longitude"),
            "isp": data.get("connection", {}).get("isp"),
            "asn": data.get("connection", {}).get("asn"),
            "country_code": data.get("country_code")
        }
    except Exception as e:
        print(f"Error fetching IP info: {e}")
        return None

@app.route('/')
def index():
    ip_info = get_ip_info()
    return render_template('index.html', ip_info=ip_info)

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)