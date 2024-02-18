from flask import Flask, render_template, request

app = Flask(__name__)

health_data = []

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        full_name = request.form.get('full_name')
        day = request.form.get('day')
        month = request.form.get('month')
        year = request.form.get('year')
        cnp = request.form.get('cnp')
        blood_pressure = request.form.get('blood_pressure')
        pulse = request.form.get('pulse')
        weight = request.form.get('weight')

        new_entry = {
            'full_name': full_name,
            'day': day,
            'month': month,
            'year': year,
            'cnp': cnp,
            'blood_pressure': blood_pressure,
            'pulse': pulse,
            'weight': weight
        }

        health_data.append(new_entry)

    return render_template('index.html')

@app.route('/view_data', methods=['GET'])
def view_data():
    return render_template('view_data.html', health_data=health_data)

@app.route('/graphs', methods=['POST'])
def show_graphs():
    selected_cnp = request.form.get('selected_cnp')

    filtered_data = [entry for entry in health_data if entry['cnp'] == selected_cnp]

    dates = [entry['day'] + '/' + entry['month'] + '/' + entry['year'] for entry in filtered_data]
    medical_fields = ['blood_pressure', 'pulse', 'weight']
    plots_data = []

    for field in medical_fields:
        health_stat = [float(entry[field]) for entry in filtered_data]

        plot_data = {
            'x': dates,
            'y': health_stat,
            'type': 'bar',
            'name': field
        }

        plots_data.append(plot_data)

    title_dict = {
        'blood_pressure': 'Evolutia tensiunii arteriale',
        'pulse': 'Evolutia pulsului',
        'weight': 'Evolutia greutatii corporale'
    }
    title = title_dict.get(medical_fields[0], 'Health Data')

    layout = {
        'barmode': 'group',
        'title': f'{title} for CNP: {selected_cnp}',
        'xaxis': {'title': 'Date'},
        'yaxis': {'title': 'Value'}
    }

    return render_template('graphs.html', plots_data=plots_data, layout=layout, cnp=selected_cnp)

@app.route('/all_data', methods=['GET'])
def view_all_data():
    return render_template('view_data.html', health_data=health_data)

@app.route('/view_data2/<int:cnp>', methods=['GET'])
def view_data2(cnp):
    filtered_data = [entry for entry in health_data if entry['cnp'] == cnp]
    return render_template('view_data2.html', filtered_data=filtered_data, cnp=cnp)

if __name__ == '__main__':
    app.run(debug=True)
