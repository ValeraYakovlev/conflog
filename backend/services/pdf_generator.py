from io import BytesIO

import qrcode
from PIL import Image
from reportlab.lib.colors import black
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from reportlab.platypus import Frame, Paragraph


def generate_qr(text):
    """
    Генераирует PIL.Image с QR.
    Здесь должен быть вызов моего модуля
    """
    return qrcode.make(text)


def create_pdf(filename, data):
    """
    Генерирует PDF с одинаковыми бейджиками с QR и текстом.
    """
    c = canvas.Canvas(filename, pagesize=A4)
    styles = getSampleStyleSheet()
    style = styles['Normal']

    badge_width = 3 * cm
    badge_height = 5 * cm
    padding = 0.5 * cm

    x, y = padding, A4[1] - badge_height - padding

    for i, item in enumerate(data):
        # Рисуем пунктирный прямоугольник вокруг бейджа
        c.setDash(3, 3)  # 3 точка, 3 пробел
        c.setStrokeColor(black)
        c.rect(x, y, badge_width, badge_height)

        c.setDash()  # возврат к нормальному контуру

        # Вставляем QR
        img = generate_qr(item['text'])
        img_buffer = BytesIO()
        img.save(img_buffer, format='PNG')
        img_buffer.seek(0)

        image = ImageReader(img_buffer)

        c.drawImage(image, x + padding, y + badge_height - padding - 4*cm, width=1*cm, height=1*cm)

        # Вставляем текст с помощью Paragraph
        p = Paragraph(item['label'], style)
        frame = Frame(x + padding, y + padding, badge_width - 2*padding, badge_height - 5*cm, showBoundary=0)
        frame.addFromList([p], c)

        c.drawString(x, y, 'проверка русского')

        # Смещаем на следующий
        x += badge_width
        if x + badge_width > A4[0]:  # если перешли правый край
            x = padding
            y -= badge_height
            if y < padding:
                c.showPage()
                y = A4[1] - badge_height - padding

    c.save()


data = [
    {"label": "Посетитель с длинными именем и информацией", "text": "https://example.com/1"},
    {"label": "What", "text": "https://example.com/2"},
    {"label": "Еще один участник с информацией на нескольких строках", "text": "https://example.com/3"},
    {"label": "Посетитель с длинными именем и информацией", "text": "https://example.com/1"},
    {"label": "What", "text": "https://example.com/2"},
    {"label": "Еще один участник с информацией на нескольких строках", "text": "https://example.com/3"},
    {"label": "Посетитель с длинными именем и информацией", "text": "https://example.com/1"},
    {"label": "What", "text": "https://example.com/2"},
    {"label": "Еще один участник с информацией на нескольких строках", "text": "https://example.com/3"}
]

create_pdf("badges_report.pdf", data)
print("Файл badges_report.pdf создан.")
