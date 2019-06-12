from flask import Flask, render_template, send_from_directory, request, flash
from flask_bootstrap import Bootstrap
from flask_script import Manager, Server
import socket
import os

SECRET_KEY = "KeepThisS3cr3t"
SITE_WIDTH = 800


app = Flask(__name__)

Bootstrap(app)
manager = Manager(app)
app.config.from_object(__name__)


manager.add_command("runserver", Server(
    use_debugger = True,
    use_reloader = True,
    host = '0.0.0.0')
)

@app.route('/',methods=['GET','POST'])
def index():
    if request.method == "POST":
        print 'test'
        print request.form
        if 'warehouse_shape' not in request.form:
            flash('Warehouse shape is required')
        shape = request.form['warehouse_shape']
        print shape
        if shape in ['wh1','wh2','wh3']:
            readers = 2
        elif shape == 'wh4':
            readers = 1
        readers_cost = readers * 4100
        dl = request.form['dimension_length']
        dw = request.form['dimension_width']
        print len(dl),len(dw)
        if len(dw)==0 or len(dl)==0:
            flash('width and length sizes are required')
            return render_template('egysystem.html')
        else:
            area = int(dl)*int(dw)
        if area <= 500:
            trucks = 3
            cartons = 120000
        elif area > 500 and area <= 1000:
            trucks = 5
            cartons = 250000
        elif area > 1000 and area <= 1500:
            trucks = 7
            cartons = 370000
        elif area > 1500:
            trucks = 10
            cartons = 500000
        pallets = cartons / 4
        printers = 3550
        system_wh = 4230
        print(shape,readers_cost,dl,dw,area,trucks,cartons,pallets,printers,system_wh)
    return render_template('egysystem.html')

@app.route('/results')
def results():
    return render_template('results.html')

@app.route('/vendor/<path:path>')
def send_vendor(path):
    return send_from_directory('vendor', path)

@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('css', path)

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)

@app.route('/fonts/<path:path>')
def send_fonts(path):
    return send_from_directory('fonts', path)

@app.route('/images/<path:path>')
def send_images(path):
    return send_from_directory('images', path)

@app.route("/healthcheck")
def healthcheck():
    return "200 OK"

if __name__ == '__main__':
    manager.run()
