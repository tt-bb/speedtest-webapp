from flask import Flask, render_template, request
import speedtest
import requests
import json
import os


app = Flask(__name__)
app.config['DEBUG'] = True


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        print("~~~ SPEEDTEST ~~~")
        print("in progress...")

        # Get IP information
        ip = request.remote_addr
        key = os.environ['KEY']
        url = f"https://ipgeolocation.abstractapi.com/v1/?api_key={key}&ip_address={ip}"
        response = requests.get(url)
        result = json.loads(response.content)

        print(f"\tFrom your IP address : {ip}")
        city = result["city"]
        print(f"\tCity : {city}")
        country = result["country"]
        print(f"\tCountry : {country}")
        fai = result["connection"]["isp_name"]
        print(f"\tFAI : {fai}")

        # Speedtest
        test = speedtest.Speedtest()

        # Speeds in bytes
        download = test.download()
        upload = test.upload()

        # Speeds in Mbps
        download *= (9.537 * (10 ** -7))
        upload *= (9.537 * (10 ** -7))
        download = round(download, 2)
        upload = round(upload, 2)

        print(f"\n\t∇ : {download} Mbps")
        print(f"\t∆ : {upload} Mbps")

        return render_template('index.html', ip=ip, city=city, country=country,
                               download=download, upload=upload, fai=fai)
    else:
        return render_template('index.html', ip="there is no place like 127.0.0.1", dooad=0, upload=0,
                               fai="---", city="---", country="---")


if __name__ == '__main__':
    app.run()
