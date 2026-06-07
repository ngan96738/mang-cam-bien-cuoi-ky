import time
import threading
import numpy as np
import serial
import tensorflow as tf
import sounddevice as sd
import librosa

# ==========================================
# 1. CAU HINH HE THONG - TINH CHINH NHAY
# ==========================================
PORT_CAM = "COM9"  # Cong COM ket noi voi Arduino R3
LABELS = ["BAO_NGAN", "NOISE", "QUAY_PHAI", "QUAY_TRAI", "ZOOM"]
SAMPLE_RATE = 16000
WINDOW_SIZE = 16000  # Bo dem 1 giay am thanh

# Dieu chinh de bat lenh nhay va chinh xac
SILENCE_THRESHOLD = 0.003    # Nguong bien do bo qua im lang
CONFIDENCE_THRESHOLD = 0.45   # Do tu tin toi thieu de chap nhan lenh
DEBOUNCE_TIME = 0.8          # Thoi gian khoa giua 2 lenh lien tiep

# Khoi tao bo dem va khoa an toan luong
audio_buffer = np.zeros(WINDOW_SIZE, dtype=np.float32)
buffer_lock = threading.Lock()
last_command_time = 0

# ==========================================
# 2. KET NOI PHAN CUNG & NAP MO HINH AI
# ==========================================
try:
    arduino = serial.Serial(port=PORT_CAM, baudrate=115200, timeout=1)
    time.sleep(2)
    print("Da ket noi thanh cong voi Arduino R3!")
except Exception as e:
    print(f"Loi ket noi Arduino (Kiem tra cong {PORT_CAM}): {e}")
    exit()

try:
    interpreter = tf.lite.Interpreter(model_path="model.tflite")
    interpreter.allocate_tensors()
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    
    in_scale, in_zero_point = input_details[0]['quantization']
    out_scale, out_zero_point = output_details[0]['quantization']
    print("Da nap mo hinh AI TFLite thanh cong!")
except Exception as e:
    print(f"Loi nap mo hinh TFLite: {e}")
    exit()

# ==========================================
# 3. THUAT TOAN XU LY LIEN TUC
# ==========================================
def audio_callback(indata, frames, time_info, status):
    global audio_buffer
    audio_samples = indata[:, 0]
    with buffer_lock:
        audio_buffer = np.roll(audio_buffer, -len(audio_samples))
        audio_buffer[-len(audio_samples):] = audio_samples

print("\nHE THONG DA KICH HOAT - NOI TOC DO BINH THUONG DE TEST...")

stream = sd.InputStream(samplerate=SAMPLE_RATE, channels=1, blocksize=1600, callback=audio_callback)

with stream:
    try:
        while True:
            time.sleep(0.1)  # Quet don toa 10 lan/giay
            
            with buffer_lock:
                current_audio = audio_buffer.copy()
                
            rms = np.sqrt(np.mean(current_audio**2))
            
            # Bo loc im lang
            if rms < SILENCE_THRESHOLD:
                print(f"[Dang nghe...] Bien do: {rms:.4f} -> Trang thai: Im lang                      ", end="\r")
                continue
            
            # Trich xuat dac trung toan hoc
            audio_scaled = current_audio * 32768.0
            mfcc = librosa.feature.mfcc(
                y=audio_scaled, 
                sr=SAMPLE_RATE, 
                n_fft=512, 
                hop_length=329, 
                n_mfcc=13, 
                n_mels=40,
                fmin=300,
                center=False
            )
            mfcc_features = mfcc.flatten()
            
            if len(mfcc_features) > 624:
                mfcc_features = mfcc_features[:624]
            elif len(mfcc_features) < 624:
                np.pad(mfcc_features, (0, 624 - len(mfcc_features)), 'constant')
                
            # Luong tu hoa dau vao
            if in_scale != 0.0:
                input_data = np.round(mfcc_features / in_scale + in_zero_point).astype(np.int8)
            else:
                input_data = mfcc_features.astype(np.int8)
            input_data = input_data.reshape(1, 624)
            
            # Chay AI doan
            interpreter.set_tensor(input_details[0]["index"], input_data)
            interpreter.invoke()
            output_data = interpreter.get_tensor(output_details[0]["index"])[0]
            
            # Giai luong tu hoa dau ra lay % thuc te
            if out_scale != 0.0:
                probabilities = (output_data.astype(np.float32) - out_zero_point) * out_scale
            else:
                probabilities = output_data
            
            predicted_index = np.argmax(probabilities)
            confidence = probabilities[predicted_index]
            command = LABELS[predicted_index]
            
            current_time = time.time()
            
            # Kich hoat khi dat do tu tin
            if command in ["QUAY_TRAI", "QUAY_PHAI", "ZOOM"] and confidence >= CONFIDENCE_THRESHOLD:
                if current_time - last_command_time > DEBOUNCE_TIME:
                    print(f"\n[Bien do: {rms:.4f}] KICH HOAT LENH -> {command} ({confidence*100:.1f}%)")
                    
                    if command == "QUAY_TRAI":
                        print("   -> Ban ky tu 'L' xuong Arduino")
                        arduino.write(b'L')
                    elif command == "QUAY_PHAI":
                        print("   -> Ban ky tu 'R' xuong Arduino")
                        arduino.write(b'R')
                    elif command == "ZOOM":
                        print("   -> Ban ky tu 'Z' xuong Arduino")
                        arduino.write(b'Z')
                        
                    last_command_time = current_time
            else:
                # Hien nhan doan nen de theo doi phan hoi cua AI
                print(f"[Dang nghe...] Bien do: {rms:.4f} -> AI doan: {command} ({confidence*100:.1f}%)         ", end="\r")

    except KeyboardInterrupt:
        print("\nDa tat he thong nhan dien.")
    finally:
        arduino.close()
        print("Da dong cong COM an toan.")