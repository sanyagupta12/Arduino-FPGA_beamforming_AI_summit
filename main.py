import serial
import struct
import wave
import numpy as np
import time

# ---------------- CONFIG ----------------
SERIAL_PORT = "COM14"
BAUD_RATE = 115200
FS = 48000
DURATION = 5            # seconds
K = 4                   # number of microphones
J = 12                  # taps
MU = 0.0005

OUT_WAV = "beamformed_output.wav"

# ---------------- BEAMFORMER MATH ----------------

def build_constraint_matrix(K, J):
    KJ = K * J
    C = np.zeros((KJ, J))
    for j in range(J):
        C[j*K:(j+1)*K, j] = 1.0
    return C

def precompute_CM_and_F(C, f):
    M = np.linalg.inv(C.T @ C)
    F = C @ (M @ f)
    return M, F

def apply_P_to_vector(v, C, M):
    return v - C @ (M @ (C.T @ v))

def frost_init(K, J, f):
    C = build_constraint_matrix(K, J)
    M, F = precompute_CM_and_F(C, f)
    W = F.copy()
    return W, C, M, F

def frost_step(W, xk, C, M, F, mu):
    yk = float(np.dot(W, xk))
    W_temp = W - mu * yk * xk
    W = apply_P_to_vector(W_temp, C, M) + F
    return yk, W

# ---------------- SERIAL ----------------

def read_multichannel_sample(ser, K):
    raw = ser.read(2 * K)
    if len(raw) != 2 * K:
        return None
    samples = struct.unpack('<' + 'h'*K, raw)
    return np.array(samples, dtype=np.float32) / 32768.0

# ---------------- MAIN ----------------

print("Opening serial...")
ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
ser.reset_input_buffer()

print("Waiting for data...")
while ser.in_waiting < 2 * K:
    time.sleep(0.01)

# Beamformer setup
f = np.zeros(J)
f[0] = 1.0  # distortionless constraint

W, C, M, F = frost_init(K, J, f)

buffer = np.zeros((J, K))
output = []

num_samples = int(FS * DURATION)

print("Streaming + Beamforming...")
for n in range(num_samples):
    x = read_multichannel_sample(ser, K)
    if x is None:
        continue

    buffer[1:, :] = buffer[:-1, :]
    buffer[0, :] = x
    xk = buffer.reshape(-1)

    yk, W = frost_step(W, xk, C, M, F, MU)
    output.append(yk)

ser.close()
print("Done streaming.")

# ---------------- SAVE WAV ----------------

output = np.array(output)
output /= np.max(np.abs(output) + 1e-9)
output_int16 = np.int16(output * 32767)

with wave.open(OUT_WAV, 'w') as wf:
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(FS)
    wf.writeframes(output_int16.tobytes())

print(f"Saved {OUT_WAV}")