import openpyxl
import random

def generate_ean13():
    # Первые 3 цифры (например, 460-469 — Россия)
    country_code = "460"
    # Генерируем 9 случайных цифр
    random_part = ''.join([str(random.randint(0, 9)) for _ in range(9)])
    # Временный код из 12 цифр (без контрольной суммы)
    temp_code = country_code + random_part
    # Рассчитываем контрольную сумму
    checksum = 0
    for i in range(12):
        digit = int(temp_code[i])
        checksum += digit * (3 if i % 2 == 1 else 1)
    checksum = (10 - (checksum % 10)) % 10
    # Полный штрихкод
    ean13 = temp_code + str(checksum)
    return ean13

# Создаем Excel-файл
wb = openpyxl.Workbook()
ws = wb.active
ws.title = "Штрихкоды"
ws.append(["№", "Штрихкод (EAN-13)"])

# Генерируем 100 штрихкодов
for i in range(1, 101):
    ws.append([i, generate_ean13()])

# Сохраняем файл
wb.save("barcodes.xlsx")
print("Файл 'штрихкоды.xlsx' успешно создан!")