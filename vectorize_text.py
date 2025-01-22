from openai import AzureOpenAI
import os
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient


def main(text,file_name):
    """テキストをベクトル化する関数"""
    # OpenAI API を使ってテキストをベクトル化

    response = AzureOpenAI.Embedding.create(
        model="text-embedding-ada-002",  # 使用するモデル
        input=text
    )
    BLOB_ACCOUNT_NAME = os.environ["BLOB_ACCOUNT_NAME"]
    BLOB_CONTAINER_NAME = os.environ["BLOB_CONTAINER_NAME"]
    
    # Cognitive Search クライアントを作成
    search_client = SearchClient(endpoint=os.environ["SEARCH_ENDPOINT"], index_name=os.environ["INDEX_NAME"], credential=AzureKeyCredential(os.environ["SEARCH_API_KEY"]))

    # インデックスにアップロードするためのドキュメントを作成
    document = {
        "@search.action": "upload",
        "id": file_name,
        "content": text,
        "vector": response['data'][0]['embedding'] ,  # ベクトルデータを追加
        "metadata_storage_path": f"https://{BLOB_ACCOUNT_NAME}.blob.core.windows.net/{BLOB_CONTAINER_NAME}/{file_name}"
    }


    # Azure Cognitive Search にインデックス化
    search_client.upload_documents(documents=[document])

    return "ベクトル化に成功しました"