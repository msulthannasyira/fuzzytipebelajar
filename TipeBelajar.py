import pandas as pd
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# Baca data dari file Excel
data = pd.read_excel('D:/fuzzy2/data.xlsx')

# Inisialisasi variabel input dan output fuzzy
visual = ctrl.Antecedent(np.arange(0, 101, 1), 'visual')
audio = ctrl.Antecedent(np.arange(0, 101, 1), 'audio')
kinestetik = ctrl.Antecedent(np.arange(0, 101, 1), 'kinestetik')
tipe_belajar = ctrl.Consequent(np.arange(0, 101, 1), 'tipe_belajar')

# Fungsi keanggotaan untuk variabel input visual
visual['rendah'] = fuzz.trimf(visual.universe, [0, 0, 50])
visual['sedang'] = fuzz.trimf(visual.universe, [0, 50, 100])
visual['tinggi'] = fuzz.trimf(visual.universe, [50, 100, 100])

# Fungsi keanggotaan untuk variabel input audio
audio['rendah'] = fuzz.trimf(audio.universe, [0, 0, 50])
audio['sedang'] = fuzz.trimf(audio.universe, [0, 50, 100])
audio['tinggi'] = fuzz.trimf(audio.universe, [50, 100, 100])

# Fungsi keanggotaan untuk variabel input kinestetik
kinestetik['rendah'] = fuzz.trimf(kinestetik.universe, [0, 0, 50])
kinestetik['sedang'] = fuzz.trimf(kinestetik.universe, [0, 50, 100])
kinestetik['tinggi'] = fuzz.trimf(kinestetik.universe, [50, 100, 100])

# Fungsi keanggotaan untuk variabel output tipe_belajar
tipe_belajar['rendah'] = fuzz.trimf(tipe_belajar.universe, [0, 0, 50])
tipe_belajar['sedang'] = fuzz.trimf(tipe_belajar.universe, [0, 50, 100])
tipe_belajar['tinggi'] = fuzz.trimf(tipe_belajar.universe, [50, 100, 100])

# Aturan fuzzy
rule1 = ctrl.Rule(visual['rendah'] & ~audio['tinggi'] & ~kinestetik['tinggi'], tipe_belajar['rendah'])
rule2 = ctrl.Rule(visual['sedang'] & audio['rendah'] & ~kinestetik['tinggi'], tipe_belajar['sedang'])
rule3 = ctrl.Rule(visual['tinggi'] & ~audio['rendah'] & kinestetik['rendah'], tipe_belajar['tinggi'])

# Buat sistem kontrol fuzzy
tipe_belajar_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])
tipe_belajar_sim = ctrl.ControlSystemSimulation(tipe_belajar_ctrl)

# Evaluasi tipe belajar
results = []
for index, row in data.iterrows():
    tipe_belajar_sim.input['visual'] = row['visual']
    tipe_belajar_sim.input['audio'] = row['audio']
    tipe_belajar_sim.input['kinestetik'] = row['kinestetik']
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
results_df.to_excel('D:/fuzzy2/output_tipe_belajar.xlsx', index=False)

