#include <Servo.h>

Servo cameraServo; 
const int servoPin = 9; // Chân D9 trên Arduino Uno sẽ nối với chân tín hiệu của Servo

void setup() {
  Serial.begin(115200); // Mở cổng Serial với tốc độ 115200 để nhận lệnh từ PC
  cameraServo.attach(servoPin);
  cameraServo.write(90); // Đặt góc mặc định cho camera ở chính giữa (90 độ)
  Serial.println("Arduino Uno R3 da san sang nhan lenh!");
}

void loop() {
  // Kiểm tra xem máy tính có gửi ký tự nào xuống không
  if (Serial.available() > 0) {
    char command = Serial.read(); // Đọc ký tự điều khiển
    
    if (command == 'L') { 
      cameraServo.write(45); // Lệnh từ PC là 'L' -> Xoay camera sang TRAI
      Serial.println("[Hanh Dong]: Camera dang xoay sang TRAI");
    } 
    else if (command == 'R') { 
      cameraServo.write(135); // Lệnh từ PC là 'R' -> Xoay camera sang PHAI
      Serial.println("[Hanh Dong]: Camera dang xoay sang PHAI");
    } 
    else if (command == 'Z') { 
      cameraServo.write(90); // Lệnh từ PC là 'Z' -> Đưa camera về GIỮA (Zoom)
      Serial.println("[Hanh Dong]: Camera ve vi tri MAC DINH");
    }
  }
}