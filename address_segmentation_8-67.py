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

        self.entity_map = {}
        
        def add_entities(entities: list[str], entity_type: str):
            for original_name in entities:
                name_lower = " ".join(original_name.lower().split())
                if not name_lower: continue
                if name_lower not in self.entity_map:
                    self.entity_map[name_lower] = {}
                self.entity_map[name_lower][entity_type] = original_name

        add_entities(self.list_province, "province")
        add_entities(self.list_ward, "ward")
        add_entities(self.list_street, "street")

        self.patterns = list(self.entity_map.keys())
        # Sort patterns by length for fuzzy matching
        self.patterns_sorted = sorted(self.patterns, key=len, reverse=True)
        
        self.automaton = daachorse.CharwiseDoubleArrayAhoCorasick(
            self.patterns, 
            match_kind=daachorse.MATCH_KIND_LEFTMOST_LONGEST
        )

    def process(self, s: str):
        s_lower = " ".join(s.lower().split())
        valid_matches = []
        
        for match in self.automaton.find(s_lower):
            start = match[0]
            end = match[1]
            pattern_id = match[2]
            pat_str = self.patterns[pattern_id]
            
            # Boundary relax logic
            left_ok, right_ok = True, True
            if start > 0:
                lc = s_lower[start-1]
                if lc.isdigit() and pat_str[0].isdigit():
                    left_ok = False
            if end < len(s_lower):
                rc = s_lower[end]
                if rc.isdigit() and pat_str[-1].isdigit():
                    right_ok = False
                    
            if left_ok and right_ok:
                pat_dict = self.entity_map[pat_str]
                valid_matches.append((start, end, pat_dict))
                
        valid_matches.sort(key=lambda x: x[0], reverse=True)
        
        result = {
            "province": None,
            "ward": None,
            "street": None,
        }
        
        used_intervals = []
        def is_overlap(st, en):
            for us, ue in used_intervals:
                if not (en <= us or st >= ue): return True
            return False

        for entity_type in ["province", "ward", "street"]:
            for st, en, pat_dict in valid_matches:
                if entity_type in pat_dict and not is_overlap(st, en):
                    result[entity_type] = pat_dict[entity_type]
                    used_intervals.append((st, en))
                    break
                    
        # Fuzzy fallback cho các thực thể bị thiếu
        missing = [k for k, v in result.items() if v is None]
        if missing:
            chars = list(s_lower)
            for st, en in used_intervals:
                for i in range(st, en):
                    chars[i] = ' '
            remaining_text = "".join(chars)
            remaining_parts = [p.strip() for p in re.split(r'[,/-]', remaining_text) if p.strip()]
            
            for etype in missing:
                best_match = None
                best_score = 0.82
                candidates = [pat for pat in self.patterns_sorted if etype in self.entity_map[pat]]
                
                for part in remaining_parts:
                    for cand in candidates:
                        score = 0
                        if len(cand) >= 4 and cand in part:
                            score = 1.0
                        else:
                            words = part.split()
                            cand_words = len(cand.split())
                            if len(words) >= cand_words:
                                for i in range(len(words) - cand_words + 1):
                                    sub = " ".join(words[i:i+cand_words])
                                    sub_score = difflib.SequenceMatcher(None, cand, sub).ratio()
                                    if sub_score > score:
                                        score = sub_score
                        if score > best_score:
                            best_score = score
                            best_match = cand
                            
                if best_match:
                    result[etype] = self.entity_map[best_match][etype]
                    
        return result