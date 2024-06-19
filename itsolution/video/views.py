from django.http import HttpResponse
from django.http import FileResponse
from .models import Message
import cv2
import numpy as np

def create_video(message):

    # Размеры видео (ширина x высота)
    width, height = 100, 100

    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    # Задаём параметры - видеопоток с частотой 24 кадра в
    out = cv2.VideoWriter("video.avi", fourcc, 24.0, (width, height))

    # Создаем кадр с черным фоном
    frame = np.zeros((height, width, 3), dtype=np.uint8)

    # Начальные координаты для бегущей строки
    x, y = width, height // 2

    # Установим параметры шрифта
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1
    font_thickness = 2
    font_color = (255, 255, 255)  # Белый цвет текста

    # Пройдемся по каждому кадру
    for t in range(24*3):  # 3 секунды с частотой 24 кадра/сек
        # Очистка кадра
        frame.fill(0)

        # Новые координаты для бегущей строки
        x -= int(1+len(message)/(3))  # Скорость бегущей строки

        # Вот тут добавим текст
        cv2.putText(frame, message, (x, y), font, font_scale, font_color, font_thickness)

        # Тут запишем кадр
        out.write(frame)

    out.release()
    cv2.destroyAllWindows()



def index(request):
    host = request.META["HTTP_HOST"]  # получаем адрес сервера
    path = request.path  # получаем запрошенный путь
    message = request.GET.get("text")
    create_video(message)
    # return HttpResponse(f"""
    #     <p>Text:{message}</p>
    #     <p>Стажёр Гагарин Игорь</p>
    # """)
    bdmessage = Message(text=message)
    bdmessage.save()
    return FileResponse(open('video.avi','rb'))