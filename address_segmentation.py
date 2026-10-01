import ahocorasick
import time

# ==========================================
# 1. PHA KHỞI TẠO (Chỉ chạy 1 lần khi Start Server)
# ==========================================

# Giả lập load dữ liệu từ Database (PostgreSQL/MySQL)
database_records = [
    ("Hồ Chí Minh", "city"),
    ("Hà Nội", "city"),
    ("Quận 1", "district"),
    ("Quận 10", "district"),
    ("Bến Nghé", "ward"),
    ("Lê Duẩn", "street")
]

# Khởi tạo Automaton
A = ahocorasick.Automaton()

# Thêm từ khóa vào cây.
# Tham số 1: Chuỗi cần tìm
# Tham số 2: Data trả về khi tìm thấy (ở đây ta lưu tuple gồm loại và tên)
for name, entity_type in database_records:
    # Lowercase để search không phân biệt hoa thường
    A.add_word(name.lower(), (entity_type, name))

# BẮT BUỘC: Biến cây Trie thành Aho-Corasick Automaton (Thêm failure links)
A.make_automaton()

print("Đã nạp xong bộ nhớ. Sẵn sàng xử lý!")

# ==========================================
# 2. PHA XỬ LÝ (Hot-path, gọi mỗi khi có Request)
# ==========================================

def segment_address(input_string):
    # Khởi tạo kết quả
    found_entities = {
        "city": [],
        "district": [],
        "ward": [],
        "street": []
    }
    
    input_lower = input_string.lower()
    
    # A.iter() quét toàn bộ chuỗi đầu vào chỉ với 1 vòng lặp (O(N) time)
    for end_index, (entity_type, original_name) in A.iter(input_lower):
        # Lưu kết quả tìm được
        found_entities[entity_type].append(original_name)
        
    return found_entities

# --- TEST HIỆU NĂNG ---
if __name__ == "__main__":
    test_string = "Số 123 đường Lê Duẩn, phường Bến Nghé, Quận 1, TP Hồ Chí Minh"
    
    start_time = time.perf_counter()
    result = segment_address(test_string)
    end_time = time.perf_counter()
    
    print("Kết quả:", result)
    print(f"Thời gian xử lý: {(end_time - start_time) * 1000:.4f} ms") 
    # Output thường sẽ là ~0.005 ms đến 0.05 ms (Nhanh gấp hàng trăm lần SLA 10ms của bạn)
