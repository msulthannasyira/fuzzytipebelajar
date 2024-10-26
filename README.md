# Implementasi Fuzzy Logic (Logika Fuzzy) Untuk Mengetahui Logika Belajar Menggunakan Python

## 1. Pendahuluan
Fuzzy Logic (Logika Fuzzy) adalah metode komputasi yang memungkinkan penggunaan nilai "kabur" atau "tidak pasti" yang lebih alami bagi manusia. Berbeda dengan logika biner yang hanya mengenal 0 atau 1, logika fuzzy bekerja dalam rentang nilai yang kontinu. Pada sistem fuzzy, sebuah nilai tidak harus absolut (benar atau salah), melainkan dapat memiliki nilai antaranya, seperti “sedikit” atau “cukup tinggi.”

Dalam studi ini, diterapkan pendekatan fuzzy untuk mengidentifikasi tipe belajar seseorang, berdasarkan hasil tiga tes yang diukur pada skala 0 hingga 100. Tes ini mencakup:

Tes 1: Menilai kecenderungan belajar visual.

Tes 2: Menilai kecenderungan belajar melalui audio.

Tes 3: Menilai kecenderungan belajar kinestetik.

## 2. Deskripsi Kode Program
Kode ini menggunakan paket skfuzzy untuk membangun sistem kontrol fuzzy yang mengidentifikasi tipe belajar seseorang berdasarkan tiga nilai input: tes1, tes2, dan tes3. Sistem ini akan memberikan hasil tipe belajar sebagai "Kinestetik", "Visual", atau "Audio" berdasarkan nilai input.

### 2.1. Impor Library dan Baca Data
```python
import pandas as pd
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
data = pd.read_excel('D:/tipe belajar/data.xlsx')
```

Kode ini mengimpor pustaka yang diperlukan untuk analisis fuzzy dan membaca data input dari file Excel `data.xlsx`.

### 2.2. Inisialisasi Variabel Input dan Output
```python
tes1 = ctrl.Antecedent(np.arange(0, 101, 1), 'tes1')
tes2 = ctrl.Antecedent(np.arange(0, 101, 1), 'tes2')
tes3 = ctrl.Antecedent(np.arange(0, 101, 1), 'tes3')
tipe_belajar = ctrl.Consequent(np.arange(0, 101, 1), 'tipe_belajar')
```

Bagian ini mendefinisikan tiga variabel input fuzzy (`tes1`, `tes2`, `tes3`) dan satu variabel output fuzzy (`tipe_belajar`) dalam rentang 0 hingga 100.

### 2.3. Definisi Fungsi Keanggotaan

Fungsi keanggotaan digunakan untuk menetapkan nilai keanggotaan rendah, sedang, dan tinggi pada masing-masing input, serta output tipe belajar.
```python
tes1['rendah'] = fuzz.trimf(tes1.universe, [0, 0, 50])
tes1['sedang'] = fuzz.trimf(tes1.universe, [0, 50, 100])
tes1['tinggi'] = fuzz.trimf(tes1.universe, [50, 100, 100])
```

Contoh di atas mendefinisikan fungsi keanggotaan untuk input tes1 menggunakan fungsi trimf (Triangular Membership Function), yang memberikan bentuk fungsi segitiga pada variabel `tes1` dengan tiga tingkat keanggotaan: rendah, sedang, dan tinggi. Pola yang sama diterapkan pada `tes2`, `tes3`, dan `tipe_belajar`.

### 2.4. Aturan Fuzzy
```python
rule1 = ctrl.Rule(tes1['rendah'] & ~tes2['tinggi'] & ~tes3['tinggi'], tipe_belajar['rendah'])
rule2 = ctrl.Rule(tes1['sedang'] & tes2['rendah'] & ~tes3['tinggi'], tipe_belajar['sedang'])
rule3 = ctrl.Rule(tes1['tinggi'] & ~tes2['rendah'] & tes3['rendah'], tipe_belajar['tinggi'])
```

Pada bagian ini, ditentukan aturan fuzzy untuk menentukan tipe belajar:

Rule 1: Jika tes1 rendah, dan tes2 serta tes3 bukan tinggi, maka tipe belajar rendah (lebih condong ke tipe kinestetik).

Rule 2: Jika tes1 sedang, tes2 rendah, dan tes3 bukan tinggi, maka tipe belajar sedang (lebih condong ke tipe visual).

Rule 3: Jika tes1 tinggi, tes2 bukan rendah, dan tes3 rendah, maka tipe belajar tinggi (lebih condong ke tipe audio).

### 2.5. Pembuatan Sistem Kontrol Fuzzy

```python
tipe_belajar_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])
tipe_belajar_sim = ctrl.ControlSystemSimulation(tipe_belajar_ctrl)
```
Bagian ini menginisialisasi sistem kontrol fuzzy dengan aturan yang sudah dibuat.

### 2.6. Evaluasi dan Simpan Hasil

```python
results = []
for index, row in data.iterrows():
    tipe_belajar_sim.input['tes1'] = row['tes1']
    tipe_belajar_sim.input['tes2'] = row['tes2']
    tipe_belajar_sim.input['tes3'] = row['tes3']
    tipe_belajar_sim.compute()
    output_value = tipe_belajar_sim.output['tipe_belajar']
    if output_value <= 33:
        output_letter = 'Kinestetik'
    elif output_value <= 66:
        output_letter = 'Visual'
    else:
        output_letter = 'Audio'
    result = {'Data ke': index+1, 'Tipe Belajar': output_letter}
    results.append(result)
```

Setiap baris data digunakan sebagai input untuk sistem fuzzy yang kemudian menghasilkan tipe belajar, disimpan dalam list `results`.

### 2.7. Menyimpan Output
```python
results_df = pd.DataFrame(results)
results_df.to_excel('D:/tipe belajar/output_tipe_belajar.xlsx', index=False)
```

Bagian terakhir menyimpan hasil klasifikasi tipe belajar ke dalam file Excel `output_tipe_belajar.xlsx`.

## 3. Kesimpulan

Metode fuzzy logic berhasil diterapkan untuk mengklasifikasikan tipe belajar berdasarkan nilai tes dengan input `tes1`, `tes2`, dan `tes3`. Hasil klasifikasi dapat membantu memahami kecenderungan belajar seseorang secara lebih alami melalui pendekatan fuzzy.
