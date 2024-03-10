import mysql.connector
from models.document import Document
from config import DATABASE_CONFIG


class DocumentRepo:
    def __init__(self):
        self.mydb = mysql.connector.connect(**DATABASE_CONFIG)
        self.create_document_table_if_not_exists()

    def create_document_table_if_not_exists(self):
        cursor = self.mydb.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS documents (
                id INT PRIMARY KEY,
                description VARCHAR(255),
                url VARCHAR(255)
            ) 
        """)
        self.mydb.commit()

    def read_all_documents(self):
        cursor = self.mydb.cursor(dictionary=True)
        sql = "SELECT * FROM documents"
        cursor.execute(sql)
        documents = cursor.fetchall()
        return documents

    def create_document(self, document: Document):
        cursor = self.mydb.cursor()
        sql = "INSERT INTO documents (id, description, url) VALUES (%s, %s, %s)"
        val = (document.id, document.description, document.url)
        cursor.execute(sql, val)
        self.mydb.commit()

    def read_document(self, document_id: int):
        cursor = self.mydb.cursor(dictionary=True)
        sql = "SELECT * FROM documents WHERE id = %s"
        val = (document_id,)
        cursor.execute(sql, val)
        document = cursor.fetchone()
        return document

    def update_document(self, document_id: int, document: Document):
        cursor = self.mydb.cursor()
        sql = "UPDATE documents SET description = %s, url = %s WHERE id = %s"
        val = (document.description, document.url, document_id)
        cursor.execute(sql, val)
        self.mydb.commit()

    def delete_document(self, document_id: int):
        cursor = self.mydb.cursor()
        sql = "DELETE FROM documents WHERE id = %s"
        val = (document_id,)
        cursor.execute(sql, val)
        self.mydb.commit()
