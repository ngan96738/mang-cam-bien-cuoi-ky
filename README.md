\# ĐỀ TÀI: Voice control camera an ninh

\*(Môn học: Mạng cảm biến)\*



\## 1. Sinh viên thực hiện

\* \*\*Họ và tên:\*\* Nguyễn Hoàng Bảo Ngân

\* \*\*Hình thức:\*\* Cá nhân



\---



\## 2. Mô tả cấu trúc thư mục \& Tệp tin

Kho lưu trữ mã nguồn bao gồm các thành phần sau:



\### Cấu phần nhúng \& Mô hình AI từ Edge Impulse:

\* `sketch\_may29a/sketch\_may29a.ino`: Mã nguồn nhúng Arduino chạy trên thiết bị phần cứng để xử lý dữ liệu mạng cảm biến.

\* `ei-kws\_giongnoi\_baongan-arduino-1.0.115-time-series-data,-audio-(mfcc),-neural-network-(keras)-#1.zip`: Thư viện mã nguồn được xuất từ Edge Impulse, chứa dữ liệu chuỗi thời gian, xử lý âm thanh (MFCC) và cấu hình mạng nơ-ron (Keras) cho bài toán nhận diện giọng nói (KWS).

\* `ei-kws\_giongnoi\_baongan-nn-classifier-tensorflow-lite-int8-quantized-model.5.lite`: Mô hình phân loại mạng nơ-ron (NN Classifier) dạng TensorFlow Lite đã được lượng tử hóa INT8 nhằm tối ưu hóa bộ nhớ trên chip nhúng.

\* `model.tflite`: File mô hình học máy TensorFlow Lite phục vụ nhận diện trực tiếp.



\### Cấu phần xử lý trên Máy tính (Python scripts):

\* `test\_camera.py`: Script Python kiểm tra luồng nhận diện và cấu hình đầu vào của camera hệ thống.

\* `check\_ai.py`: Script Python kiểm tra độc lập và đánh giá hoạt động của mô hình AI.

\* `final\_app.py`: Ứng dụng chính tích hợp luồng xử lý và giao diện hệ thống.

\* `run\_system.py`: Script Python tổng thể dùng để kích hoạt vận hành toàn bộ hệ thống mạng cảm biến.



\---



\## 3. Các phụ thuộc (Dependencies)



\### Môi trường Phần cứng / Vi điều khiển:

\* Phần mềm \*\*Arduino IDE\*\* (Khuyến nghị phiên bản 2.x trở lên).

\* Thư viện Edge Impulse dạng ZIP (được đính kèm sẵn trong kho lưu trữ) để tích hợp vào Arduino IDE.



\### Môi trường Máy tính (Python):

Hệ thống chạy trên nền tảng \*\*Python 3\*\*, yêu cầu cài đặt trước các thư viện phụ thuộc sau:

\* `opencv-python` (Phục vụ xử lý dữ liệu hình ảnh trong `test\_camera.py`)

\* `tensorflow` hoặc `tflite-runtime` (Phục vụ nạp và chạy các mô hình `.tflite`, `.lite`)

\* `numpy` (Xử lý và tính toán mảng dữ liệu)

\* `pyserial` (Hỗ trợ giao tiếp nối tiếp qua cổng COM giữa vi điều khiển và máy tính)



\---



\## 4. Hướng dẫn cài đặt và vận hành



\### Bước 1: Cài đặt thư viện Python phụ thuộc

Mở Terminal/CMD tại thư mục dự án và thực hiện lệnh:

```bash

pip install opencv-python tensorflow numpy pyserial

```

\### Bước 2: Nạp mã nguồn cho Vi điều khiển

Khởi động Arduino IDE.

Thêm thư viện AI bằng cách vào Sketch -> Include Library -> Add .ZIP Library... rồi chọn tệp tin ei-kws\_giongnoi\_baongan-...zip có sẵn trong thư mục.

Mở tệp tin sketch\_may29a/sketch\_may29a.ino, lựa chọn đúng cấu hình mạch, cổng kết nối (COM port) và tiến hành Biên dịch \& Nạp code (Upload) xuống thiết bị.



\### Bước 3: Vận hành hệ thống trên máy tính

Đảm bảo thiết bị vi điều khiển đã kết nối với máy tính.

Kiểm tra hoạt động của camera bằng lệnh:

```bash

python test\_camera.py

```

Khởi chạy toàn bộ hệ thống đồng bộ bằng lệnh:

```bash

python run\_system.py

```

