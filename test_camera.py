import serial
import time

# =================================================================
# LƯU Ý: Bạn phải đổi chữ 'COM3' thành đúng cổng COM của Arduino Uno 
# mà bạn đang xem trong phần mềm Arduino IDE (ví dụ: 'COM4', 'COM5'...)
# =================================================================
PORT_CAM = 'COM9' 

try:
    # Mở cổng kết nối với Arduino
    arduino = serial.Serial(port=PORT_CAM, baudrate=115200, timeout=1)
    time.sleep(2) # Đợi 2 giây để mạch Arduino khởi động lại sau khi kết nối
    print("=== ĐÃ KẾT NỐI THÀNH CÔNG VỚI ARDUINO UNO R3 ===")
    
    # 1. Thử nghiệm ra lệnh QUAY TRÁI
    print("\n[AI PC]: Phát hiện lệnh 'quay_trai' -> Gửi lệnh sang Arduino...")
    arduino.write(b'L') # Gửi ký tự 'L' xuống mạch
    time.sleep(3)       # Chờ 3 giây xem servo quay
    
    # 2. Thử nghiệm ra lệnh QUAY PHẢI
    print("\n[AI PC]: Phát hiện lệnh 'quay_phai' -> Gửi lệnh sang Arduino...")
    arduino.write(b'R') # Gửi ký tự 'R' xuống mạch
    time.sleep(3)       # Chờ 3 giây xem servo quay
    
    # 3. Thử nghiệm đưa về VỊ TRÍ MẶC ĐỊNH (ZOOM)
    print("\n[AI PC]: Phát hiện lệnh 'zoom' -> Đưa camera về mặc định...")
    arduino.write(b'Z') # Gửi ký tự 'Z' xuống mạch
    time.sleep(2)
    
    print("\n=== KIỂM TRA HOÀN TẤT! ===")
    arduino.close() # Đóng kết nối

except Exception as e:
    print(f"LỖI KẾT NỐI: Hãy kiểm tra lại cổng COM hoặc tắt cửa sổ Serial Monitor cũ đi nhé! Chi tiết: {e}")