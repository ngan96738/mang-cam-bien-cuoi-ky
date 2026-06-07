import time
import numpy as np
import serial
import tensorflow as tf

# 1. Cấu hình Cổng COM Arduino và Danh sách Nhãn AI
PORT_CAM = "COM9"  # Đúng cổng COM của bạn lúc nãy
LABELS = ["BAO_NGAN", "NOISE", "QUAY_PHAI", "QUAY_TRAI", "ZOOM"]

# 2. Kết nối tới mạch Arduino
try:
    arduino = serial.Serial(port=PORT_CAM, baudrate=115200, timeout=1)
    time.sleep(2)  # Chờ mạch khởi động ổn định
    print("🟢 Đã kết nối thành công với Arduino R3!")
except Exception as e:
    print(f"🔴 Lỗi kết nối Arduino (Hãy kiểm tra cổng {PORT_CAM} hoặc tắt Arduino IDE): {e}")
    exit()

# 3. Nạp mô hình AI
interpreter = tf.lite.Interpreter(model_path="model.tflite")
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
print("🟢 Đã nạp mô hình AI thành công!")


# Hàm phụ trợ: Nhận mảng số đặc trưng âm thanh -> AI dự đoán -> Ra lệnh cho Arduino
def predict_and_control(input_features):
    # Đảm bảo dữ liệu đầu vào đúng kiểu int8 và đúng ma trận [1, 624]
    input_data = np.array(input_features, dtype=np.int8).reshape(1, 624)

    # Đưa dữ liệu vào mô hình và chạy AI
    interpreter.set_tensor(input_details[0]["index"], input_data)
    interpreter.invoke()

    # Lấy kết quả đầu ra
    output_data = interpreter.get_tensor(output_details[0]["index"])[0]

    # Tìm xem nhãn nào có tỷ lệ chính xác cao nhất (vị trí index)
    predicted_index = np.argmax(output_data)
    command = LABELS[predicted_index]

    print(f"\n[AI PC]: Nhận diện được từ khóa -> 🔥 {command} 🔥")

    # Điều khiển Arduino dựa theo kết quả AI nhận diện
    if command == "QUAY_TRAI":
        print("-> Gửi lệnh 'L' sang Arduino...")
        arduino.write(b"L")
    elif command == "QUAY_PHAI":
        print("-> Gửi lệnh 'R' sang Arduino...")
        arduino.write(b"R")
    elif command == "ZOOM":
        print("-> Gửi lệnh 'Z' sang Arduino...")
        arduino.write(b"Z")
    else:
        print("-> Từ khóa phụ hoặc tiếng ồn (NOISE), không điều khiển.")


# --- TEST THỬ LOGIC HỆ THỐNG ---
print("\n--- Chạy thử nghiệm giả lập 1 lệnh QUAY_TRAI ---")
# Tạo thử một mảng giả lập 624 phần tử để test xem Arduino có quay không
fake_audio_features = np.zeros(624, dtype=np.int8)

# Giả sử mô hình đoán ra nhãn QUAY_TRAI (index số 3 trong danh sách LABELS)
# Ta gán giá trị lớn tại index số 3 để ép mô hình nhận diện ra QUAY_TRAI
output_details = interpreter.get_output_details()

# Chạy hàm test luôn
predict_and_control(fake_audio_features)

# Đóng kết nối khi dừng
arduino.close()