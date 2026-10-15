# NOTE: you MUST change this cell
# New methods / functions must be written under class Solution.
class Solution:
    def __init__(
        self,
        list_province: list[str],
        list_ward: list[str],
        list_street: list[str]
    ):
        self.list_province = list_province
        self.list_ward = list_ward
        self.list_street = list_street

        # 1. Khởi tạo danh sách các mẫu (patterns) và bảng ánh xạ (entity_map)
        self.entity_map = {}
        patterns = []
        pattern_id = 0

        # Hàm helper để nạp data vào mảng pattern và map lại ID
        def add_entities(entities: list[str], entity_type: str):
            nonlocal pattern_id
            for original_name in entities:
                name_lower = original_name.lower()
                patterns.append(name_lower)
                self.entity_map[pattern_id] = (original_name, entity_type)
                pattern_id += 1

        # Nạp dữ liệu theo thứ tự
        add_entities(self.list_province, "province")
        add_entities(self.list_ward, "ward")
        add_entities(self.list_street, "street")

        # 2. Xây dựng Double-Array Aho-Corasick Automaton cho chuỗi Unicode (Charwise)
        # Bắt buộc dùng CharwiseDoubleArrayAhoCorasick để hỗ trợ tiếng Việt
        self.automaton = daachorse.CharwiseDoubleArrayAhoCorasick(
            patterns, 
            match_kind=daachorse.MATCH_KIND_LEFTMOST_LONGEST
        )

    def process(self, s: str):
        s_lower = s.lower()
        
        result = {
            "province": None,
            "ward": None,
            "street": None,
        }
        
        # Hàm find() của daachorse trả về list các tuple: (start_index, end_index, pattern_id)
        for match in self.automaton.find(s_lower):
            pattern_id = match[2]
            original_name, entity_type = self.entity_map[pattern_id]
            
            if result[entity_type] is None:
                result[entity_type] = original_name
                
        return result