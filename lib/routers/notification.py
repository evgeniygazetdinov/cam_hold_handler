from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
import pandas as pd
import barcode
from barcode.writer import ImageWriter
import reportlab.lib.pagesizes as pagesizes
from reportlab.pdfgen import canvas
import os

app = FastAPI()


@app.post("/generate-labels/")
async def generate_labels(file: UploadFile = File(...)):
    # 1. Читаем Excel
    df = pd.read_excel(file.file)

    # 2. Генерируем штрихкоды и сохраняем в PNG
    barcode_images = []
    for code in df["Код маркировки"]:
        ean = barcode.get("code128", code, writer=ImageWriter())
        filename = f"barcode_{code}"
        ean.save(filename)
        barcode_images.append(f"{filename}.png")

    # 3. Создаем PDF с этикетками
    pdf_path = "labels.pdf"
    c = canvas.Canvas(pdf_path, pagesize=pagesizes.A4)

    x, y = 50, 750  # Стартовая позиция
    for i, (img_path, row) in enumerate(zip(barcode_images, df.itertuples())):
        c.drawImage(img_path, x, y, width=100, height=50)
        c.drawString(x, y - 20, f"Название: {row.Название_товара}")
        c.drawString(x, y - 40, f"Цена: {row.Цена} ₽")

        if i % 2 == 1:  # 2 этикетки в ряд
            x = 50
            y -= 100
        else:
            x += 200

    c.save()

    # 4. Удаляем временные файлы
    for img in barcode_images:
        os.remove(img)

    return FileResponse(pdf_path)
