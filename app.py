from flask import Flask, request, render_template
import csv, io
from esm_calculations import esm_correction_fixed, esm_correction_profile, exponential_soc_profile, linear_bd_profile

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['csvfile']
        method = request.form['method']
        stream = io.StringIO(file.stream.read().decode('utf-8'))
        reader = csv.DictReader(stream)
        results = []
        for row in reader:
            bd_i = float(row['bd_i']); soc_i = float(row['soc_i'])
            bd_n = float(row['bd_n']); soc_n = float(row['soc_n'])
            depth = float(row.get('depth', 30))
            if method == 'fixed':
                Da, orig, corr = esm_correction_fixed(bd_i, soc_i, bd_n, soc_n, depth)
            else:
                inc = 1
                bd_i_p = linear_bd_profile(bd_i, bd_i, depth, inc)
                soc_i_p = exponential_soc_profile(soc_i, soc_i, depth, 0, inc)
                bd_n_p = linear_bd_profile(bd_n, bd_n, depth, inc)
                soc_n_p = exponential_soc_profile(soc_n, soc_n, depth, 0, inc)
                corr = esm_correction_profile(bd_i_p, soc_i_p, bd_n_p, soc_n_p, depth, inc)
                Da, orig = None, None
            results.append({'bd_i': bd_i, 'soc_i': soc_i, 'bd_n': bd_n, 'soc_n': soc_n,
                            'depth': depth, 'adjusted_depth': Da, 'corrected_stock': corr})
        return render_template('results.html', results=results, method=method)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
