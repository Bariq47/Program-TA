import numpy as np
import pandas as pd
from datetime import datetime

# =======================================================
# 1. Generate timestamp 1 bulan (interval 10 detik)
# =======================================================

start_time = datetime.now()
timestamps = pd.date_range(start=start_time, periods=259200, freq="10S")
# 259200 = 30 hari data dengan interval 10 detik

N = len(timestamps)

# =======================================================
# 2. Rasio kondisi
# =======================================================

normal_ratio = 0.50
warning_ratio = 0.20
danger_ratio = 0.30

normal_n = int(N * normal_ratio)
warning_n = int(N * warning_ratio)
danger_n = N - normal_n - warning_n

# =======================================================
# 3. Threshold ranges parameter SAG Mill
# =======================================================

ranges = {
    "[CPM]TESM_018.oValue": {
        "normal": (0, 110),
        "warning": (110, 120),
        "danger": (121, 160)
    },
    "[CPM]TESM_025.oValue": {
        "normal": (0, 110),
        "warning": (110, 120),
        "danger": (121, 160)
    },
    "[CPM]TESM_019.oValue": {
        "normal": (0, 130),
        "warning": (130, 155),
        "danger": (156, 200)
    },
    "[CPM]TESM_020.oValue": {
        "normal": (0, 130),
        "warning": (130, 155),
        "danger": (156, 200)
    },
    "[CPM]TESM_021.oValue": {
        "normal": (0, 130),
        "warning": (130, 155),
        "danger": (156, 200)
    },
    "[CPM]TESM_022.oValue": {
        "normal": (0, 130),
        "warning": (130, 155),
        "danger": (156, 200)
    },
    "[CPM]TESM_023.oValue": {
        "normal": (0, 130),
        "warning": (130, 155),
        "danger": (156, 200)
    },
    "[CPM]TESM_024.oValue": {
        "normal": (0, 130),
        "warning": (130, 155),
        "danger": (156, 200)
    },
    "[CPM]RPM_SM": {
        "normal": (0, 13),
        "warning": (13, 14),
        "danger": (14, 16)
    },
    "[CPM]MOTOR_CURRENT_SM.ioRawValue": {
        "normal": (0, 250),
        "warning": (250, 296),
        "danger": (297, 350)
    }
}

params = list(ranges.keys())


# =======================================================
# 4. Helper function
# =======================================================

def sample_value(param, status):
    low, high = ranges[param][status]
    return np.random.uniform(low, high)


# =======================================================
# 5. Generate NORMAL data
# =======================================================

data = []

for i in range(normal_n):

    row = {}

    for p in params:
        row[p] = sample_value(p, "normal")

    data.append(row)


# =======================================================
# 6. Generate WARNING data
# hanya beberapa parameter naik
# =======================================================

for i in range(warning_n):

    row = {}

    # pilih parameter yang warning
    faulty_params = np.random.choice(params, size=2, replace=False)

    for p in params:

        if p in faulty_params:
            row[p] = sample_value(p, "warning")
        else:
            row[p] = sample_value(p, "normal")

    data.append(row)


# =======================================================
# 7. Generate DANGER data
# =======================================================

for i in range(danger_n):

    row = {}

    faulty_params = np.random.choice(params, size=4, replace=False)

    for p in params:

        if p in faulty_params:
            row[p] = sample_value(p, "danger")
        else:
            row[p] = sample_value(p, "normal")

    data.append(row)


# =======================================================
# 8. Convert ke DataFrame
# =======================================================

df = pd.DataFrame(data)

# Tambahkan timestamp
df["timestamp"] = timestamps

# Reorder kolom
cols = ["timestamp"] + params
df = df[cols]

# =======================================================
# 9. Simpan dataset
# =======================================================

df.to_csv("dummy_sagmill_dataset5.csv", index=False)

print("Dataset created")
print(df.shape)
print(df.head())

