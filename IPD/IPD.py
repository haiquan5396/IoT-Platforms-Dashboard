from flask import Flask
from flask.templating import render_template
from platform_driver import openhab,home_assistant
app = Flask(__name__)


@app.route('/')
def layout():
    return render_template('layout.html')

@app.route('/about/')
def about():
    return render_template('about.html')

@app.route('/home/')
def home():
    return render_template('home.html')
@app.route('/test')
def test():
    # oh = openhab.openhab_driver()
    # print oh.get_sensor_state("Light1")
    # print oh.set_sensor_state("Light1","OFF")
    ha = home_assistant.home_assistant()
    print ha.set_sensor_state("switch.garage_ceiling_light","on")
    return render_template('home.html')


if __name__ == '__main__':
    app.run()
