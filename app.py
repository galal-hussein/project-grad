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
        if 'warehouse_shape' not in request.form:
            flash('Warehouse shape is required')
            return render_template('egysystem.html', form=request.form)
        if 'req_sys' not in request.form:
            flash('Required system is required')
            return render_template('egysystem.html', form=request.form)
        if 'receive' not in request.form:
            flash('Product receiving system is required')
            return render_template('egysystem.html', form=request.form)
        receive = request.form['receive']
        shape = request.form['warehouse_shape']
        if shape in ['wh1','wh2','wh3']:
            readers = 2
        elif shape == 'wh4':
            readers = 1
        readers_cost = readers * 4100
        dl = request.form['dimension_length']
        dw = request.form['dimension_width']
        if 'shifts' not in request.form:
            flash('shifts per day number is required')
            return render_template('egysystem.html', form=request.form)
        shifts_per_day =  request.form['shifts']

        if len(dw)==0 or len(dl)==0:
            flash('width and length sizes are required')
            return render_template('egysystem.html', form=request.form)
        else:
            area = int(dl)*int(dw)
        if area <= 500:
            trucks = 3
            forklift_trucks = 1
            cartons = 120000
        elif area > 500 and area <= 1000:
            trucks = 5
            forklift_trucks = 2
            cartons = 250000
        elif area > 1000 and area <= 1500:
            trucks = 7
            forklift_trucks = 3
            cartons = 370000
        elif area > 1500:
            trucks = 10
            forklift_trucks = 3
            cartons = 500000
        pallets = cartons / 4
        workers = trucks * int(shifts_per_day)
        printers = 1
        printers_cost = 3550
        system_wh = 4230
        handheld_numbers = int(workers) / 2
        handheld_cost = 3250 * handheld_numbers
        trucks_readers_cost = 3655 * forklift_trucks
        results = {
        "shape": shape,
        "space": area,
        "trucks": trucks,
        "trucks_readers": forklift_trucks,
        "trucks_readers_cost": trucks_readers_cost,
        "handhelds": handheld_numbers,
        "handheld_cost": handheld_cost,
        "workers": workers,
        "receive": receive,
        "cartons": cartons,
        "pallets": pallets,
        "gate_readers": readers,
        "gate_readers_cost": readers_cost,
        "printers": printers,
        "printers_cost": printers_cost,
        "wh_sys": system_wh,
        }
        return render_template('results.html',results=results)
    return render_template('egysystem.html', form=request.form)

@app.route('/results')
def results():
    return render_template('results.html')

@app.route('/totalcost', methods=['GET','POST'])
def totalcost():
    total_cost = 0
    if request.method == "POST":
        try:
            trucks = request.form['trucks']
            trucks_readers = request.form['trucks_readers']
            handhelds = request.form['handhelds']
            workers = request.form['workers']
            if pallets in request.form:
                pallets = request.form['pallets']
            if cartons in request.form:
                cartons = request.form['cartons']
            gate_readers = request.form['gate_readers']
            printers = request.form['printers']


            # calc costs
            trucks_readers_cost = 3655 * int(trucks_readers)
            handheld_cost = 3250 * int(handhelds)
            gate_readers_cost = int(gate_readers) * 4100
            printers_cost = 3550 * int(printers)
            system_wh = 4230
            tag_cost = (int(pallets) * 0.31) + (int(cartons) * 0.31)
            total_cost = tag_cost+ trucks_readers_cost + handheld_cost + gate_readers_cost + printers_cost +system_wh
        except:
            flash('error in calculating total cost, please revise the numbers')
            return render_template('total_cost.html', total_cost=total_cost)
        return render_template('total_cost.html', total_cost=total_cost)




        receive = request.form['receive']
        shape = request.form['warehouse_shape']
        if shape in ['wh1','wh2','wh3']:
            readers = 2
        elif shape == 'wh4':
            readers = 1
        readers_cost = readers * 4100
        dl = request.form['dimension_length']
        dw = request.form['dimension_width']
        if 'shifts' not in request.form:
            flash('shifts per day number is required')
            return render_template('egysystem.html', form=request.form)
        shifts_per_day =  request.form['shifts']

        if len(dw)==0 or len(dl)==0:
            flash('width and length sizes are required')
            return render_template('egysystem.html', form=request.form)
        else:
            area = int(dl)*int(dw)
        if area <= 500:
            trucks = 3
            forklift_trucks = 1
            cartons = 120000
        elif area > 500 and area <= 1000:
            trucks = 5
            forklift_trucks = 2
            cartons = 250000
        elif area > 1000 and area <= 1500:
            trucks = 7
            forklift_trucks = 3
            cartons = 370000
        elif area > 1500:
            trucks = 10
            forklift_trucks = 3
            cartons = 500000
        pallets = cartons / 4
        workers = trucks * int(shifts_per_day)
        printers = 1
        printers_cost = 3550
        system_wh = 4230
        handheld_numbers = int(workers) / 2
        handheld_cost = 3250 * handheld_numbers
        trucks_readers_cost = 3655 * forklift_trucks
        results = {
        "shape": shape,
        "space": area,
        "trucks": trucks,
        "trucks_readers": forklift_trucks,
        "trucks_readers_cost": trucks_readers_cost,
        "handhelds": handheld_numbers,
        "handheld_cost": handheld_cost,
        "workers": workers,
        "receive": receive,
        "cartons": cartons,
        "pallets": pallets,
        "gate_readers": readers,
        "gate_readers_cost": readers_cost,
        "printers": printers,
        "printers_cost": printers_cost,
        "wh_sys": system_wh,
        }
        return render_template('results.html',results=results)
    return render_template('total_cost.html')

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
