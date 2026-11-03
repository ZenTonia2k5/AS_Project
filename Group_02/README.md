# G_02 – Address Entity Recognition

Chương trình nhận diện **Province, Ward và Street** từ chuỗi địa chỉ bằng thuật toán **Aho-Corasick** (`daachorse`).

## Processing Flow

![Processing Flow](processing_flow.png)

## Run with Google Colab

1. Mở [`G_02.ipynb`](https://colab.research.google.com/drive/1zrGDObIwB3exO5nfQoMPCgaU-3LvGQ_4) hoặc upload notebook lên [Google Colab](https://colab.research.google.com/).
2. Chọn **Runtime → Run all**.
3. Notebook tự cài thư viện, tải dữ liệu test và database từ Google Drive, chạy đánh giá.
4. Sau khi chạy xong, file kết quả `G_02.xlsx` được tạo. File gồm hai sheet: `summary` và `details`.

Cần có kết nối Internet để tải dữ liệu từ Google Drive.

## Run with Python (.py)

### 1. Prepare environment

Cài Python và mở Terminal tại thư mục project. Nên tạo virtual environment:

```bash
python -m venv .venv
```

Kích hoạt môi trường:

**macOS / Linux**
```bash
source .venv/bin/activate
```

**Windows**
```powershell
.venv\Scripts\activate
```

Cài các thư viện cần thiết:

```bash
python -m pip install --upgrade pip
python -m pip install daachorse pandas xlsxwriter editdistance gdown
```

### 2. Prepare data files

Đặt các file sau cùng thư mục với `g_02.py`:

```text
test.json
list_province.txt
list_ward.txt
list_street.txt
```

Có thể tải các file bằng lệnh sau trong Terminal:

```bash
gdown --fuzzy "https://drive.google.com/file/d/18qzaHmx9-fcKPi4gTq304G2JvXy_g6XW/view?usp=sharing" -O test.json
gdown --fuzzy "https://drive.google.com/file/d/1PHRkRLRaO2vFivLbcPJsaxjvZ7K_I3lU/view?usp=drive_link" -O list_province.txt
gdown --fuzzy "https://drive.google.com/file/d/1QrSouYn6IUEW7Impje1vOxzsksjlAJ-h/view?usp=drive_link" -O list_ward.txt
gdown --fuzzy "https://drive.google.com/file/d/1yP2dBE8K9QtUiaLPewtQRr-hDH0gOgfa/view?usp=drive_link" -O list_street.txt
```

### 3. Run the script

**Note:** `g_02.py` is exported from the Colab notebook and currently contains notebook shell commands beginning with `!` (such as `!pip`, `!rm`, and `!gdown`). These commands are not valid in a normal Python script. Run the installation and download commands above in Terminal, then remove the corresponding `!` command cells/lines from `g_02.py` before running it.

Run:

```bash
python g_02.py
```

The script writes the evaluation workbook `G_02.xlsx` in the current directory.

## Output

`Solution.process(address)` returns:

```python
{
    "province": "Ho Chi Minh",
    "ward": "Ben Nghe",
    "street": "Nguyen Hue"
}
```

A field is `None` when no matching entity is selected.
