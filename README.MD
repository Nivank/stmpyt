# 🛰 STM32 Ultrasonic Radar Visualization

![Python](https://img.shields.io/badge/Python-3.12-blue)
![STM32CubeIDE](https://img.shields.io/badge/STM32CubeIDE-Latest-green)

Real-time **ultrasonic sensor visualization** using STM32 and Python.  
Displays distance as a **radar view** (0°–180°) and **distance vs time graph** with spike detection.

---

## 📷 Screenshots

**Radar View**  
![Radar Screenshot](docs/radar_screenshot.png)

**Distance vs Time Graph**  
![Graph Screenshot](docs/graph_screenshot.png)

---

## 🛠 Hardware Setup

**Microcontroller:** STM32 (Nucleo or F4 series)  
**Sensor:** HC-SR04 Ultrasonic  

### Pin Connections

| Sensor Pin | STM32 Pin | Description              |
|------------|-----------|--------------------------|
| VCC        | 5V / 3.3V | Power supply             |
| GND        | GND       | Ground                   |
| TRIG       | PA0       | Trigger pin              |
| ECHO       | PA1       | Echo pin (input capture) |

**Optional LED:**  
- LD2 → PA5 (onboard LED)

---

## ⏱ STM32 Configuration

- **Timer (TIM2):** For microsecond delays  
  - Prescaler: 83  
  - Period: 0xFFFFFFFF  

- **UART (USART2):** For serial data  
  - Baud rate: 115200  
  - Word length: 8 bits, 1 stop bit, no parity  

- **GPIO:**  
  - TRIG: Output  
  - ECHO: Input  

STM32 sends distance via UART in **cm**, one value per line:
120
95
102


---

## 💻 Python Visualization

### Features

- **Radar view** (filtered distance in blue, spikes in red)  
- **Distance vs Time graph** with spike annotations  
- FIR filter for smoothing  

### Dependencies

- Python 3.10+  
- `pyserial`  
- `matplotlib`  
- `numpy`  

Install via:

```bash
pip install -r requirements.txt

Set the correct COM port in Python:
ser = serial.Serial("COM9", 115200)

🚀 Usage

Flash STM32 firmware with CubeIDE

Connect the board to PC via USB

Run Python visualization: python sensor_ultrasonic.py
⚙️ Customization

Radar range: ax_radar.set_ylim()

Spike threshold: SPIKE_THRESHOLD in Python

FIR filter weights: fir_coeffs
