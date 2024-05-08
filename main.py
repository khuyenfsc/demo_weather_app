import requests
from flask import Flask, render_template, request, flash, url_for, redirect
informations = []
def get_infor(city_name):
    response_infors = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API}").json()
    return response_infors

app = Flask(__name__)
app.config['SECRET_KEY'] = 'thesecretmakesawomanattraction'
@app.route('/')
def error_noti():
    return render_template('weather.html')
@app.route('/', methods=['GET', 'POST'])
def get_city():
    city_name = request.form.get('city_name')
    response_infors = get_infor(city_name)
    print(response_infors)
    error_msg = ''
    if response_infors['cod'] == '404':
        error_msg = 'City does not exist!'
    if error_msg == '':
        informations = [
            {
                'name' : city_name,
                'description' : response_infors['weather'][0]['description'],
                'temp' : int(response_infors['main']['temp']) - 273,
                'icon' : f"https://openweathermap.org/img/wn/{response_infors['weather'][0]['icon']}@2x.png"
            }
        ]
        return render_template('weather.html', informations=informations)
    flash(error_msg, 'error')
    return redirect(url_for('error_noti'))
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)