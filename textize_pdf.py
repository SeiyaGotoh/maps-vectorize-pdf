
import fitz  # PyMuPDF
import easyocr

# PDFを処理する関数
def main(pdf_path):
    # EasyOCRリーダーの初期化（英語と日本語）
    reader = easyocr.Reader(['ja'])
    extracted_text = ""

    # PDFを開く
    doc = fitz.open(pdf_path)
    for page_num in range(len(doc)):
        # ページを画像に変換
        page = doc.load_page(page_num)
        pix = page.get_pixmap(dpi=300)  # 高解像度に設定
        image_bytes = pix.tobytes("ppm")

        # OCRでテキスト抽出
        results = reader.readtext(image_bytes)
        for result in results:
            extracted_text += result[1] + "\n"

    return extracted_text
