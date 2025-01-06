from datetime import datetime
import logging
import azure.functions as func
import tempfile
import os
from textize_pdf import main as textize_pdf
from vectorize_text import main as vectorize_text

app = func.FunctionApp()

@app.route(route="maps/vectorize", auth_level=func.AuthLevel.FUNCTION)
# HTTPトリガー関数
def vectorize(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('HTTP trigger function received a request.')

    try:
        # PDFファイルの取得
        req_body = req.files['file']
        if not req_body:
            return func.HttpResponse("PDFファイルが必要です。", status_code=400)

        # 一時ファイルに保存
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file.write(req_body.stream.read())
            tmp_file_path = tmp_file.name

        # テキスト抽出
        text = textize_pdf(tmp_file_path)
        text=""

        message = vectorize_text(text,f"{datetime.now().timestamp()}.jpg")

        # 一時ファイルを削除
        os.remove(tmp_file_path)

        return func.HttpResponse(text, status_code=200, mimetype="text/plain")

    except Exception as e:
        logging.error(f"エラー発生: {str(e)}")
        return func.HttpResponse(f"エラーが発生しました: {str(e)}", status_code=500)
