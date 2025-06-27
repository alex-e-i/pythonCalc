import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from math import pi
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import datetime
import csv


# Компоненты модели
components = [
    "Цифровые технологии",
    "Индивидуальный профиль",
    "Диагностика",
    "Внешние агенты",
    "Базовые потребности",
    "Навыки саморегуляции",
    "Оценка и коррекция"
]

# Веса компонентов
weights = {
    "Цифровые технологии": 0.15,
    "Индивидуальный профиль": 0.1,
    "Диагностика": 0.15,
    "Внешние агенты": 0.15,
    "Базовые потребности": 0.15,
    "Навыки саморегуляции": 0.15,
    "Оценка и коррекция": 0.2
}


class MotivationCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Калькулятор мотивации спортсменов")

        # Словарь для хранения ползунков
        self.sliders = {}

        # Создаем поля ввода
        for i, comp in enumerate(components):
            tk.Label(root, text=comp).grid(row=i, column=0, padx=10, pady=5, sticky="w")
            slider = tk.Scale(root, from_=0, to=10, orient="horizontal", resolution=0.1)
            slider.set(5)
            slider.grid(row=i, column=1, padx=10, pady=5)
            self.sliders[comp] = slider

        # Кнопка расчёта
        self.calc_button = tk.Button(root, text="Рассчитать мотивацию", command=self.calculate)
        self.calc_button.grid(row=len(components), column=0, columnspan=1, pady=10)

        # Кнопка сохранения
        self.save_button = tk.Button(root, text="Сохранить данные", command=self.save_data)
        self.save_button.grid(row=len(components), column=1, columnspan=1, pady=10)

        # Место для графика
        self.canvas = None
        self.motivation_score = 0

    def calculate(self):
        # Получаем значения из слайдеров
        values = {comp: float(self.sliders[comp].get()) for comp in components}

        # Рассчитываем общий уровень мотивации
        self.motivation_score = sum(weights[comp] * values[comp] for comp in components)

        # Отображаем результат
        result_text = f"Уровень мотивации: {self.motivation_score:.2f} / 10"
        print(result_text)
        messagebox.showinfo("Результат", result_text)

        # Рисуем график
        self.plot_radar(values)

    def plot_radar(self, data):
        labels = list(data.keys())
        stats = list(data.values())

        angles = [n / float(len(labels)) * 2 * pi for n in range(len(labels))]
        stats += stats[:1]
        angles += angles[:1]

        fig, ax = plt.subplots(figsize=(5, 5), subplot_kw=dict(polar=True))
        ax.fill(angles, stats, color='skyblue', alpha=0.4)
        ax.plot(angles, stats, color='blue', linewidth=2)

        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(labels)
        ax.yaxis.set_ticklabels([])

        plt.title("Мотивационный профиль спортсмена")

        # Интегрируем в Tkinter
        if hasattr(self, 'canvas') and self.canvas:
            self.canvas.get_tk_widget().destroy()
        self.canvas = FigureCanvasTkAgg(fig, master=self.root)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=0, column=2, rowspan=len(components)+1)

    def save_data(self):
        if self.motivation_score == 0:
            messagebox.showwarning("Ошибка", "Сначала рассчитайте уровень мотивации.")
            return

        # Получаем текущие значения
        values = {comp: float(self.sliders[comp].get()) for comp in components}
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Предлагаем путь для сохранения файла
        file_path = filedialog.asksaveasfilename(defaultextension=".csv",
                                                  filetypes=[("CSV файл", "*.csv"), ("Текстовый файл", "*.txt")],
                                                  title="Сохранить данные спортсмена")

        if not file_path:
            return  # Пользователь отменил сохранение

        if file_path.endswith('.csv'):
            # Сохранение в CSV
            with open(file_path, mode='w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['Дата и время', 'Параметр', 'Значение'])
                writer.writerow([timestamp, 'Общий уровень мотивации', f"{self.motivation_score:.2f}/10"])
                for key, value in values.items():
                    writer.writerow([timestamp, key, value])
            messagebox.showinfo("Сохранено", f"Данные успешно сохранены в:\n{file_path}")

        elif file_path.endswith('.txt'):
            # Сохранение в TXT
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(f"Дата и время: {timestamp}\n")
                f.write(f"Общий уровень мотивации: {self.motivation_score:.2f}/10\n\n")
                f.write("Параметры:\n")
                for key, value in values.items():
                    f.write(f"- {key}: {value}\n")
            messagebox.showinfo("Сохранено", f"Данные успешно сохранены в:\n{file_path}")

        else:
            messagebox.showerror("Ошибка", "Неверный формат файла. Выберите .csv или .txt")


if __name__ == "__main__":
    root = tk.Tk()
    app = MotivationCalculator(root)
    root.mainloop()