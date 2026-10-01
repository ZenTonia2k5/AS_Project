"""
Synthetic Dataset Generator for Address Segmentation.
Generates realistic Vietnamese address data matching Slide 7 & 8 specifications:
- 34 provinces
- 10 wards per province
- Streets per ward (~70)
- 1000 sample addresses in all_raw.json with realistic variations:
  * Regular addresses (House number, Street, Ward, Province)
  * Alley numbers (e.g. 56/33, 69/49/59)
  * OCR noise (merged words: HCần Giuộc, Tlong An, ThuanThanh)
  * Abbreviations (LTK, TP. HCM, HN)
  * Unknown/missing wards (Diên Hồng not in Ward DB -> ward: null)
"""
import os
import sys
import json
import random

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

PROVINCES_34 = [
    "Thành phố Hồ Chí Minh", "Thành phố Hà Nội", "Thành phố Đà Nẵng",
    "Thành phố Hải Phòng", "Thành phố Cần Thơ", "Tỉnh Long An",
    "Tỉnh Bình Dương", "Tỉnh Đồng Nai", "Tỉnh Bà Rịa - Vũng Tàu",
    "Tỉnh Tiền Giang", "Tỉnh Bến Tre", "Tỉnh Đồng Tháp",
    "Tỉnh Vĩnh Long", "Tỉnh Trà Vinh", "Tỉnh An Giang",
    "Tỉnh Kiên Giang", "Tỉnh Cà Mau", "Tỉnh Bạc Liêu",
    "Tỉnh Sóc Trăng", "Tỉnh Hậu Giang", "Tỉnh Lâm Đồng",
    "Tỉnh Khánh Hòa", "Tỉnh Bình Thuận", "Tỉnh Ninh Thuận",
    "Tỉnh Thừa Thiên Huế", "Tỉnh Quảng Nam", "Tỉnh Quảng Ngãi",
    "Tỉnh Bình Định", "Tỉnh Phú Yên", "Tỉnh Thanh Hóa",
    "Tỉnh Nghệ An", "Tỉnh Hà Tĩnh", "Tỉnh Quảng Bình", "Tỉnh Quảng Trị"
]

WARDS_TEMPLATE = [
    "Phường Bến Thành", "Phường Đa Kao", "Phường Tân Định",
    "Phường Bến Nghé", "Phường Cầu Kho", "Phường Cô Giang",
    "Xã Thuận Thành", "Xã Long Hậu", "Xã Phước Lại", "Xã Mỹ Lộc"
]

DISTRICTS_TEMPLATE = [
    "Quận 1", "Quận 3", "Quận 5", "Quận 10", "Quận Tân Bình",
    "Huyện Cần Giuộc", "Huyện Bến Lức", "Huyện Cần Đước", "Huyện Đức Hòa", "Thị xã Tân Uyên"
]

STREETS_TEMPLATE = [
    "Nam Kỳ Khởi Nghĩa", "Lý Thường Kiệt", "Nguyễn Huệ", "Lê Lợi",
    "Trần Hưng Đạo", "Cách Mạng Tháng Tám", "Hai Bà Trưng", "Điện Biên Phủ",
    "Nguyễn Thị Minh Khai", "Võ Văn Tần", "Pasteur", "Lê Duẩn",
    "Đồng Khởi", "Hàm Nghi", "Tôn Đức Thắng", "Phan Chu Trinh",
    "Sư Vạn Hạnh", "Ba Tháng Hai", "Hoàng Diệu", "Trần Phú",
    "Nguyễn Trãi", "Phan Đăng Lưu", "Bạch Đằng", "Nguyễn Đình Chiểu",
    "Huỳnh Thúc Kháng", "Phan Đình Phùng", "Lý Tự Trọng", "Trương Định",
    "Nguyễn Văn Cừ", "Võ Thị Sáu", "Trần Quốc Toản", "Ngô Quyền"
]


def generate_data(output_dir: str):
    os.makedirs(output_dir, exist_ok=True)
    random.seed(42)

    # 1. list_province.txt
    prov_file = os.path.join(output_dir, "list_province.txt")
    with open(prov_file, "w", encoding="utf-8") as f:
        for p in PROVINCES_34:
            f.write(f"{p}\n")
    print(f"Generated {len(PROVINCES_34)} provinces in {prov_file}")

    # 2. list_district.txt
    dist_file = os.path.join(output_dir, "list_district.txt")
    with open(dist_file, "w", encoding="utf-8") as f:
        for p in PROVINCES_34:
            for d in DISTRICTS_TEMPLATE[:5]:
                f.write(f"{d}\t{p}\n")
    print(f"Generated districts in {dist_file}")

    # 3. list_ward.txt (10 wards per province)
    ward_file = os.path.join(output_dir, "list_ward.txt")
    province_wards = {}
    with open(ward_file, "w", encoding="utf-8") as f:
        for p in PROVINCES_34:
            province_wards[p] = []
            for i, w in enumerate(WARDS_TEMPLATE):
                w_name = f"{w}" if "Thành phố Hồ Chí Minh" in p or "Long An" in p else f"{w} {i+1}"
                province_wards[p].append(w_name)
                f.write(f"{w_name}\t{p}\n")
    print(f"Generated 10 wards per province in {ward_file}")

    # 4. list_street.txt (~70 streets per ward)
    street_file = os.path.join(output_dir, "list_street.txt")
    with open(street_file, "w", encoding="utf-8") as f:
        for p in PROVINCES_34:
            for w in province_wards[p]:
                for s in STREETS_TEMPLATE:
                    f.write(f"{s}\t{w}\t{p}\n")
    print(f"Generated streets in {street_file}")

    # 5. all_raw.json (1000 sample queries with ground truths)
    samples = []
    # Add exact examples from slides first!
    slide_examples = [
        # Slide 8 examples
        {
            "address": "53 Nam Kỳ Khởi Nghĩa, Phường Bến Thành, Thành phố Hồ Chí Minh",
            "result": {
                "street": "Nam Kỳ Khởi Nghĩa",
                "ward": "Phường Bến Thành",
                "province": "Thành phố Hồ Chí Minh"
            }
        },
        {
            "address": "56/33 Nam Kỳ Khởi Nghĩa, Phường Bến Thành, Thành phố Hồ Chí Minh",
            "result": {
                "street": "Nam Kỳ Khởi Nghĩa",
                "ward": "Phường Bến Thành",
                "province": "Thành phố Hồ Chí Minh"
            }
        },
        {
            "address": "69/49/59 Nam Kỳ Khởi Nghĩa, Phường Bến Thành, Thành phố Hồ Chí Minh",
            "result": {
                "street": "Nam Kỳ Khởi Nghĩa",
                "ward": "Phường Bến Thành",
                "province": "Thành phố Hồ Chí Minh"
            }
        },
        # Slide 6 Example 1
        {
            "address": "268 Lý Thường Kiệt, Diên Hồng, TP. HCM",
            "result": {
                "street": "Lý Thường Kiệt",
                "ward": "Diên Hồng",
                "province": "Thành phố Hồ Chí Minh"
            }
        },
        # Slide 6 Example 2 (Abbreviation and ward null)
        {
            "address": "268 Lý Thường Kiệt, Phường Diên Hồng, TP. HCM",
            "result": {
                "street": "Lý Thường Kiệt",
                "ward": None,  # Not in database
                "province": "Thành phố Hồ Chí Minh"
            }
        },
        # Slide 5 OCR examples
        {
            "address": "X. Thuận Thành, H. Cần Giuộc, T. Long An",
            "result": {
                "street": None,
                "ward": "Xã Thuận Thành",
                "province": "Tỉnh Long An"
            }
        },
        {
            "address": "Thuận Thanh, HCần Giuộc, Tlong An",
            "result": {
                "street": None,
                "ward": "Xã Thuận Thành",
                "province": "Tỉnh Long An"
            }
        },
        {
            "address": "X ThuanThanh H. Can Giuoc, Long An",
            "result": {
                "street": None,
                "ward": "Xã Thuận Thành",
                "province": "Tỉnh Long An"
            }
        }
    ]
    samples.extend(slide_examples)

    # House number generators
    house_numbers = [
        "12", "45", "102", "268", "53", "84A", "10B",
        "56/33", "69/49/59", "12/4/8", "154/22", "30/2A"
    ]

    # Generate remaining to reach 1000
    while len(samples) < 1000:
        p = random.choice(PROVINCES_34)
        w = random.choice(province_wards[p])
        s = random.choice(STREETS_TEMPLATE)
        h = random.choice(house_numbers)

        # Style variation
        style = random.randint(0, 5)
        if style == 0:
            # Standard comma separated
            addr = f"{h} {s}, {w}, {p}"
            samples.append({
                "address": addr,
                "result": {"street": s, "ward": w, "province": p}
            })
        elif style == 1:
            # Abbreviated province (TP. HCM, HN)
            p_abbr = "TP. HCM" if p == "Thành phố Hồ Chí Minh" else ("HN" if p == "Thành phố Hà Nội" else p)
            addr = f"{h} {s}, {w}, {p_abbr}"
            samples.append({
                "address": addr,
                "result": {"street": s, "ward": w, "province": p}
            })
        elif style == 2:
            # Street abbreviation (LTK, NKKN, 3/2)
            if s == "Lý Thường Kiệt":
                s_abbr = "LTK"
            elif s == "Nam Kỳ Khởi Nghĩa":
                s_abbr = "NKKN"
            elif s == "Ba Tháng Hai":
                s_abbr = "3/2"
            else:
                s_abbr = s
            addr = f"{h} {s_abbr}, {w}, {p}"
            samples.append({
                "address": addr,
                "result": {"street": s, "ward": w, "province": p}
            })
        elif style == 3:
            # OCR noise (missing comma or space)
            addr = f"{h} {s} {w}, {p}"
            samples.append({
                "address": addr,
                "result": {"street": s, "ward": w, "province": p}
            })
        elif style == 4:
            # Without accents
            from address_segmentation.normalizer import remove_accents
            addr = f"{h} {remove_accents(s)}, {remove_accents(w)}, {remove_accents(p)}"
            samples.append({
                "address": addr,
                "result": {"street": s, "ward": w, "province": p}
            })
        else:
            # With 'Đường' prefix
            addr = f"{h} Đường {s}, {w}, {p}"
            samples.append({
                "address": addr,
                "result": {"street": s, "ward": w, "province": p}
            })

    raw_file = os.path.join(output_dir, "all_raw.json")
    with open(raw_file, "w", encoding="utf-8") as f:
        json.dump(samples, f, ensure_ascii=False, indent=2)
    print(f"Generated {len(samples)} samples in {raw_file}")


if __name__ == "__main__":
    out_dir = os.path.join(os.path.dirname(__file__))
    generate_data(out_dir)
