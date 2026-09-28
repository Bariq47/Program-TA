from fastapi import FastAPI
import numpy as np

app = FastAPI()

Q = np.load("qtable_final.npy") #1500 Episode (real)
# Q = np.load("qtable_finalDummy.npy") #1500 Episode (dummy)


def classify_temp_bearing(temp):
    if temp <= 110:
        return 0  # Normal
    elif 110 < temp <= 120:
        return 1  # Waspada
    else:
        return 2  # Bahaya

def classify_temp_winding(temp):
    if temp <= 130:
        return 0  # Normal
    elif 130 < temp <= 155:
        return 1  # Waspada
    else:
        return 2  # Bahaya

def classify_speed(speed):
    if speed <= 13:
        return 0  # Normal
    elif 13 < speed <= 14:
        return 1  # Waspada
    else:
        return 2  # Bahaya

def classify_current(current):
    if current <= 250:
        return 0  # Normal
    elif 250 < current <= 296:
        return 1  # Waspada
    else:
        return 2  # Bahaya


def get_state(data):
    return max([
        classify_temp_bearing(data["[CPM]TESM_018.oValue"]),
        classify_temp_bearing(data["[CPM]TESM_025.oValue"]),
        classify_temp_winding(data["[CPM]TESM_019.oValue"]),
        classify_temp_winding(data["[CPM]TESM_020.oValue"]),
        classify_temp_winding(data["[CPM]TESM_021.oValue"]),
        classify_temp_winding(data["[CPM]TESM_022.oValue"]),
        classify_temp_winding(data["[CPM]TESM_023.oValue"]),
        classify_temp_winding(data["[CPM]TESM_024.oValue"]),
        classify_speed(data["[CPM]RPM_SM"]),
        classify_current(data["[CPM]MOTOR_CURRENT_SM.ioRawValue"])
    ])

action_map = {
    0: "Lanjutkan Operasi",
    1: "Peringatan Dini",
    2: "Berhentikan Operasi"
}
# =========================
# API ENDPOINT
# =========================

@app.post("/predict")
def predict(data: dict):

    state = get_state(data)

    action = int(np.argmax(Q[state]))

    return {
        "time_stamp": data["time_stamp"],
        "state": state,
        "action": action,
        "action_description": action_map[action],
        "q_values": Q[state].tolist()
    }

@app.get("/qtable")
def show_qtable():
    return {
        "q_table": Q.tolist(),
        "shape": Q.shape
    }
