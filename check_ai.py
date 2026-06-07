import tensorflow as tf

try:
    # Nạp mô hình vào bộ nhớ bằng thư viện TensorFlow đầy đủ
    interpreter = tf.lite.Interpreter(model_path="model.tflite")
    interpreter.allocate_tensors()
    
    print("\n🟢 THÀNH CÔNG! Mô hình đã nạp vào Python mượt mà, không bị lỗi.")
    
    # Xem cấu trúc đầu vào của mô hình
    input_details = interpreter.get_input_details()
    print("👉 Kiểu dữ liệu mô hình cần:", input_details[0]['dtype'])
    print("👉 Số lượng phần tử đầu vào:", input_details[0]['shape'])

except Exception as e:
    print("\n🔴 LỖI RỒI: Khả năng cao là sai tên file hoặc lỗi thư viện.")
    print("Chi tiết lỗi:", e)