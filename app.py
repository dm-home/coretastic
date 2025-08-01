from flask import Flask, request, render_template
import csv, io, os
import pandas as pd
from esm_calculations import esm_correction_fixed, esm_correction_profile
from esm_calculations import exponential_soc_profile, linear_bd_profile

app = Flask(__name__)
DATA_PATH = os.path.join(os.path.dirname(__file__), 'data', 'default.xlsx')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['csvfile']
        method = request.form['method']
        stream = io.StringIO(file.stream.read().decode('utf-8'))
        reader = csv.DictReader(stream)
        results = []
        for row in reader:
            bd_i = float(row['bd_i'])
            soc_i = float(row['soc_i'])
            bd_n = float(row['bd_n'])
            soc_n = float(row['soc_n'])
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
                Da, orig = (None, None)
            results.append({'bd_i': bd_i, 'soc_i': soc_i,
                            'bd_n': bd_n, 'soc_n': soc_n,
                            'depth': depth, 'adjusted_depth': Da,
                            'corrected_stock': corr})
        return render_template('results.html', results=results, method=method)

    df = pd.read_excel(DATA_PATH, header=5).iloc[1:].reset_index(drop=True)
    results = []
    for i in range(0, len(df)-1, 2):
        base = df.iloc[i]
        new = df.iloc[i+1]
        depth = float(base['Depth _cm'])
        bd_i = float(base['BD _g/cm3'])
        soc_i = float(base['SOC_%']) / 100
        bd_n = float(new['BD _g/cm3'])
        soc_n = float(new['SOC_%']) / 100
        Da, orig, corr = esm_correction_fixed(bd_i, soc_i, bd_n, soc_n, depth)
        results.append({
            'bd_i': bd_i,
            'soc_i': soc_i,
            'bd_n': bd_n,
            'soc_n': soc_n,
            'depth': depth,
            'adjusted_depth': Da,
            'corrected_stock': corr * 1e4
        })
    return render_template('results.html', results=results, method='fixed (default)')

if __name__ == '__main__':
    app.run(debug=True)
