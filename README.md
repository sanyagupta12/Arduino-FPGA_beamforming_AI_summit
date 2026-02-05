# 🎧 Real-Time Adaptive Beamforming Using the Frost Algorithm  
*A Multi-Microphone Audio Enhancement System*

---

## 🌟 Overview

This project implements a **real-time adaptive beamformer** using the **Frost constrained LMS algorithm**, operating directly on **live multi-microphone audio streams** received over a serial interface.

The system:
- Streams **synchronized audio samples from 4 microphones**
- Applies **adaptive spatial filtering** to suppress noise and interference
- Preserves sound from a **desired look direction**
- Outputs a **clean, single-channel enhanced audio signal**
- Saves the processed output as a `.wav` file for analysis or playback

The core idea is simple but powerful:  
> *Let the system continuously learn the acoustic environment and automatically suppress unwanted sound while keeping the desired signal intact.*

---

## 🧠 Why the Frost Algorithm?

Unlike simple delay-and-sum beamforming, the **Frost algorithm** introduces **hard linear constraints** that guarantee:
- **Distortionless response** in the desired direction
- **Adaptive noise minimization** elsewhere
- **Numerical stability over long runtimes**

This makes it ideal for **assistive listening, smart audio capture, and embedded real-time systems**, as originally described in Frost’s seminal 1972 work on constrained adaptive arrays.

---

## 🎯 Primary Application: Hearing Aid / Assistive Listening Device

This project is **primarily designed with hearing aids in mind**.

### Problem
People with hearing loss often struggle not because sounds are quiet—but because **everything is loud at once**:
- Background chatter
- Traffic
- Room reverberation
- Competing speakers

### Solution
This system behaves like a **software-defined directional ear**:
- Focuses on the speaker **directly in front of the listener**
- Suppresses noise from other directions
- Continuously adapts as the environment changes

### Why This Matters
✔️ Clear speech in noisy environments  
✔️ No need for pre-recorded calibration  
✔️ Works in real time  
✔️ Suitable for low-power embedded hardware  

---

## 🧩 Additional Applications

### 🗣️ Smart Conference Room Speaker System

- Button-controlled or motorized steering
- Focuses on the active speaker
- Suppresses keyboard noise, HVAC, and side conversations

### 🎓 Classroom Lecture Recording Device

- Directional capture of instructor audio
- Noise suppression in large rooms
- Clean recordings for online education and accessibility

---

## 🧱 System Architecture




---

## ⚙️ Key Parameters

| Parameter | Description |
|--------|------------|
| `K` | Number of microphones |
| `J` | FIR taps per microphone |
| `FS` | Sampling frequency |
| `MU` | Adaptation step size |
| `DURATION` | Recording length |
| `SERIAL_PORT` | Input device |
| `OUT_WAV` | Output file |

---

## 🧠 Algorithm Highlights

- Online learning (no prior noise statistics)
- Hard linear constraints
- Error-correcting weight updates
- Stable long-term operation

---

## 📁 Output

- Mono WAV file
- Normalized audio
- Ready for playback or ML pipelines

---

## 🚀 Future Extensions

- Dynamic beam steering
- Embedded ARM/DSP deployment
- Multi-beam outputs
- Neural post-filtering

---

## 📜 Reference

- O. L. Frost III, *An Algorithm for Linearly Constrained Adaptive Array Processing*, Proceedings of the IEEE, 1972


