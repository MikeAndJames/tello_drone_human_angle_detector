# 💻 Ryze Tello Field Guide: Chromebook (Intel N100 + Linux Crostini)

This guide covers everything you need to run your autonomous drone code on your **Intel N100 Chromebook (8GB RAM)** tomorrow.

---

## 🚀 1. One-Time Linux Setup (Crostini Terminal)

Open the **Terminal** app on your Chromebook and run:

```bash
# 1. Update package list and install OpenCV / Python Linux dependencies
sudo apt update && sudo apt install -y python3-pip python3-venv libgl1 libglib2.0-0

# 2. Clone your repository (or copy your folder over)
cd ~
git clone <YOUR-GITHUB-REPO-URL> drone-project
cd drone-project

# 3. Create and activate Python virtual environment
python3 -m venv venv
source venv/bin/activate

# 4. Install dependencies
pip install djitellopy opencv-python numpy
```

---

## 📡 2. Connecting to the Tello on ChromeOS

1. Power on the Tello drone (wait for flashing yellow LED).
2. Click the **Network / Wi-Fi icon** in the bottom-right corner of your Chromebook shelf.
3. Select **`TELLO-XXXXXX`** and click **Connect**.
4. ChromeOS will automatically route local UDP packets (ports `8889`, `8890`, `11111`) directly into your Crostini Linux container.

---

## 🔊 3. Cross-Platform Sound Notice (Windows vs Linux)

In `dronecapture.py`:
- `winsound.Beep()` is a Windows-only module.
- On Linux / Chromebook, you can simply use:
  ```python
  # Linux compatible lock-on alert
  print("\a")  # Triggers the Chromebook terminal bell!
  ```
  *(Or wrap it in a `try...except ImportError` so it works seamlessly on both OSes!)*

---

## 🏎️ 4. Intel N100 Performance Expectations

- **Live Stream + Denoising (`cv2.bilateralFilter`)**: ~30 FPS smooth display.
- **Haar Cascade Face Detection**: ~40–60 FPS (<15% CPU load).
- **YOLOv8 Nano (Tomorrow's Upgrade)**: ~30–45 FPS on N100 CPU cores using PyTorch / ONNX Runtime.

---

## 🎯 5. Running Your Script

Inside your activated venv:

```bash
python dronecapture.py
```

Have fun flying at the grandparents' house! 🚁👵👴
