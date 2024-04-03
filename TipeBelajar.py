import pandas as pd
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# Baca data dari file Excel
data = pd.read_excel('D:/tipe belajar/data.xlsx')

# Inisialisasi variabel input dan output fuzzy
tes1 = ctrl.Antecedent(np.arange(0, 101, 1), 'tes1')
tes2 = ctrl.Antecedent(np.arange(0, 101, 1), 'tes2')
tes3 = ctrl.Antecedent(np.arange(0, 101, 1), 'tes3')
tipe_belajar = ctrl.Consequent(np.arange(0, 101, 1), 'tipe_belajar')

# Fungsi keanggotaan untuk variabel input tes1 (visual)
tes1['rendah'] = fuzz.trimf(tes1.universe, [0, 0, 50])
tes1['sedang'] = fuzz.trimf(tes1.universe, [0, 50, 100])
tes1['tinggi'] = fuzz.trimf(tes1.universe, [50, 100, 100])

# Fungsi keanggotaan untuk variabel input tes2 (audio)
tes2['rendah'] = fuzz.trimf(tes2.universe, [0, 0, 50])
tes2['sedang'] = fuzz.trimf(tes2.universe, [0, 50, 100])
tes2['tinggi'] = fuzz.trimf(tes2.universe, [50, 100, 100])

# Fungsi keanggotaan untuk variabel input tes3 (kinestetik)
tes3['rendah'] = fuzz.trimf(tes3.universe, [0, 0, 50])
tes3['sedang'] = fuzz.trimf(tes3.universe, [0, 50, 100])
tes3['tinggi'] = fuzz.trimf(tes3.universe, [50, 100, 100])

# Fungsi keanggotaan untuk variabel output tipe_belajar
tipe_belajar['rendah'] = fuzz.trimf(tipe_belajar.universe, [0, 0, 50])
tipe_belajar['sedang'] = fuzz.trimf(tipe_belajar.universe, [0, 50, 100])
tipe_belajar['tinggi'] = fuzz.trimf(tipe_belajar.universe, [50, 100, 100])

# Aturan fuzzy
rule1 = ctrl.Rule(tes1['rendah'] & ~tes2['tinggi'] & ~tes3['tinggi'], tipe_belajar['rendah'])
rule2 = ctrl.Rule(tes1['sedang'] & tes2['rendah'] & ~tes3['tinggi'], tipe_belajar['sedang'])
rule3 = ctrl.Rule(tes1['tinggi'] & ~tes2['rendah'] & tes3['rendah'], tipe_belajar['tinggi'])

# Buat sistem kontrol fuzzy
tipe_belajar_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])
tipe_belajar_sim = ctrl.ControlSystemSimulation(tipe_belajar_ctrl)

# Evaluasi tipe belajar
results = []
for index, row in data.iterrows():
    tipe_belajar_sim.input['tes1'] = row['tes1']
    tipe_belajar_sim.input['tes2'] = row['tes2']
    tipe_belajar_sim.input['tes3'] = row['tes3']
    tipe_belajar_sim.compute()
    output_value = tipe_belajar_sim.output['tipe_belajar']
    if output_value <= 33:
        output_letter = 'Kinestetik'  # Kinestetik
    elif output_value <= 66:
        output_letter = 'Visual'  # Visual
    else:
        output_letter = 'Audio'  # Audio
    result = {'Data ke': index+1, 'Tipe Belajar': output_letter}
    results.append(result)

# Simpan hasil ke file Excel
results_df = pd.DataFrame(results)
results_df.to_excel('D:/tipe belajar/output_tipe_belajar.xlsx', index=False)


