import time  #Модуль для замера времени работы
import os  #Модуль для проверки существования файла
import wave  #Модуль для чтения wav-файлов

import numpy as np  #Библиотека для работы с массивами
import matplotlib.pyplot as plt  #Библиотека для построения графиков
from scipy.fft import dst  #Функция дискретного синусного преобразования


#Функция для ввода положительного целого числа
def read_positive_int(prompt):

    while True:
        value = input(prompt).strip()  #Считывание строки
        try:
            number = int(value)  #Преобразование строки в целое число
            if number <= 0:
                print("Ошибка: введите положительное целое число.")
                continue  #Если число не положительное, просим ввести заново
            return number
        except ValueError:
            print("Ошибка: нужно ввести целое число.")  #Ошибка, если введено не целое число

#Функция чтения wav файла
def read_wav_file(filename):

    if not os.path.exists(filename):
        raise FileNotFoundError(f"Файл '{filename}' не найден.")  #Ошибка, если файла нет

    with wave.open(filename, "rb") as wav_file:  #Открытие wav файла в режим чтения
        n_channels = wav_file.getnchannels()  #Получаем количество каналов
        sample_width = wav_file.getsampwidth()  #Получаем размер одного отсчета в байтах
        sample_rate = wav_file.getframerate()  #Получаем частоту дискретизации
        n_frames = wav_file.getnframes()  #Получаем количество кадров
        raw_data = wav_file.readframes(n_frames)  #Считываем все данные из файла

    if sample_width != 2:
        raise ValueError("Поддерживаются только WAV-файлы PCM signed 16 bit.")  #Проверка на 16 bit

    signal = np.frombuffer(raw_data, dtype=np.int16)  #Перевод байт в массив чисел int16

    return signal, sample_rate  #Возвращаем сигнал и частоту дискретизации

#Функция построения графика дискретных отсчетов
def plot_discrete_samples(signal, count):

    x = np.arange(count)  #Массив номеров отсчетов
    y = signal[:count]  #Берем первые count отсчетов

    plt.figure(figsize=(10, 5))  #Создание окна графика
    plt.axhline(0, color="black", linewidth=1)  #Рисуем горизонтальную линию y=0

    for i in range(count):
        plt.vlines(x[i], 0, y[i], linewidth=1)  #Рисуем вертикальную линию для каждого отсчета
        plt.fill_between([x[i] - 0.2, x[i] + 0.2], [y[i], y[i]], 0)  #Закрашиваем область под отсчетом

    plt.plot(x, y, marker="o", linewidth=1)  #Соединение точек линией
    plt.title("Дискретные отсчеты звукового сигнала")  #Заголовок графика
    plt.xlabel("Номер отсчета")  #Подпись оси x
    plt.ylabel("Амплитуда")  #Подпись оси y
    plt.grid(True)  #Включаем сетку
    plt.tight_layout()  #Автоматическое выравнивание элементов графика

#Функция построения осциллограммы сигнала
def plot_oscillogram(signal, sample_rate):

    time_axis = np.arange(len(signal)) / sample_rate  #Перевод номеров отсчетов во время

    plt.figure(figsize=(10, 5))  #Создание окна графика
    plt.plot(time_axis, signal)  #Построение графика амплитуды от времени
    plt.title("Осциллограмма звукового сигнала")  #Заголовок графика
    plt.xlabel("Время, с")  #Подпись оси x
    plt.ylabel("Амплитуда")  #Подпись оси y
    plt.grid(True)  #Включаем сетку
    plt.tight_layout()  #Автоматическое выравнивание элементы графика

#Функция построения спектра сигнала
def plot_dst_spectrum(signal, sample_rate):

    spectrum = dst(signal.astype(float), type=2, norm="ortho")  #Выполнение DST
    frequencies = np.arange(len(spectrum)) * sample_rate / (2 * len(spectrum))  #Формирование оси частот

    plt.figure(figsize=(10, 5))  #Создание окна графика
    plt.plot(frequencies, np.abs(spectrum))  #Построение графика спектра
    plt.title("Спектральный анализ сигнала (дискретное синусное преобразование)")  #Заголовок
    plt.xlabel("Частота, Гц")  #Подпись оси x
    plt.ylabel("Амплитуда спектра")  #Подпись оси y
    plt.grid(True)  #Включаем сетку
    plt.tight_layout()  #Автоматическое выравнивание элементов графика

#Функция построения гистограммы отсчетов сигнала
def plot_histogram(signal):

    plt.figure(figsize=(10, 5))  #Создание окна графика
    plt.hist(signal, bins=50)  #Потроегние гистограммы по 50 интервалам
    plt.title("Гистограмма отсчетов звукового сигнала")  #Заголовок графика
    plt.xlabel("Амплитуда, у.е.")  #Подпись оси x
    plt.ylabel("Количество отсчетов")  #Подпись оси y
    plt.grid(True)  #Включаем сетку
    plt.tight_layout()  #Автоматическое выравнивание элементов графика


def main():

    start_time = time.time()  #Запоминаем время начала работы программы

    filename = input("Введите имя WAV-файла: ").strip()  #Ввод имени файла
    sample_count = read_positive_int("Введите количество отсчетов для визуализации: ")  #Ввод числа отсчетов

    try:
        signal, sample_rate = read_wav_file(filename)  #Чтение сигнала и частоты дискретизации

        print()
        print(f"Файл успешно прочитан.")
        print(f"Количество отсчетов в файле: {len(signal)}")
        print(f"Частота дискретизации: {sample_rate} Гц")

        if sample_count > len(signal):
            print("Введенное количество отсчетов больше длины сигнала.")
            print(f"Будет использовано максимальное доступное количество: {len(signal)}")
            sample_count = len(signal)  #Если число больше, просто берем максимум

        plot_discrete_samples(signal, sample_count)  #Построение графика дискретных отсчетов
        plot_oscillogram(signal, sample_rate)  #Построение осциллограммы
        plot_dst_spectrum(signal, sample_rate)  #Построение спектра сигнала
        plot_histogram(signal)  #Построение гистограммы

        plt.show()  #Показ всех графикок

    except FileNotFoundError as error:
        print(f"Ошибка: {error}")  #Ошибка, если файл не найден
    except wave.Error:
        print("Ошибка: файл не является корректным WAV-файлом.")  #Ошибка формата файла
    except ValueError as error:
        print(f"Ошибка: {error}")  #Ошибка некорректного значения
    except Exception as error:
        print(f"Непредвиденная ошибка: {error}")  #Обработка любой другой ошибки

    print(time.time() - start_time, "seconds")  #Вывод времени выполнения

main()