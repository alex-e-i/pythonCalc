import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from math import pi
import pandas as pd
import datetime

# Настройки страницы
st.set_page_config(page_title="Калькулятор мотивации спортсменов", layout="wide")
st.title("🧮 Калькулятор мотивации спортсменов к УТЗ")

# Описание
st.markdown("""
Это интерактивный калькулятор модели формирования мотивации спортсменов к учебно-тренировочным занятиям 
на этапе спортивной специализации с применением цифровых технологий.
""")

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

# Боковая панель для ввода данных
st.sidebar.header("🎛️ Установите значения от 0 до 10")

values = {}
for comp in components:
    values[comp] = st.sidebar.slider(comp, min_value=0.0, max_value=10.0, value=5.0, step=0.1)

# Рассчитываем уровень мотивации
motivation_score = sum(weights[comp] * values[comp] for comp in components)

# Отображаем результат
st.subheader("📊 Результат")
st.metric(label="Уровень мотивации", value=f"{motivation_score:.2f} / 10")

# Радарная диаграмма
def plot_radar(data):
    labels = list(data.keys())
    stats = list(data.values())

    angles = [n / float(len(labels)) * 2 * pi for n in range(len(labels))]
    stats += stats[:1]
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    ax.fill(angles, stats, color='skyblue', alpha=0.4)
    ax.plot(angles, stats, color='blue', linewidth=2)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels)
    ax.yaxis.set_ticklabels([])

    plt.title("Мотивационный профиль спортсмена", size=20, pad=30)
    return fig

fig = plot_radar(values)
st.pyplot(fig)

# Сохранение данных
st.sidebar.markdown("---")
st.sidebar.subheader("💾 Сохранить данные")

if st.sidebar.button("Сохранить в CSV"):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    data_to_save = {
        "Параметр": components + ["Общий уровень мотивации"],
        "Значение": list(values.values()) + [motivation_score]
    }
    df = pd.DataFrame(data_to_save)
    csv = df.to_csv(index=False)
    st.sidebar.download_button(
        label="📥 Скачать CSV",
        data=csv,
        file_name=f"motivation_profile_{timestamp}.csv",
        mime="text/csv"
    )

# Информация о модели
with st.expander("ℹ️ Подробнее о модели"):
    st.markdown("""
    Модель включает следующие ключевые элементы:
    
    - **Цифровые технологии**: дневники, датчики, видео, платформы
    - **Индивидуальный мотивационный профиль**
    - **Диагностика**: мотивация, тревожность, отношение к УТП, социометрия и др.
    - **Навыки саморегуляции**: целеполагание, самоанализ, волевое поведение
    - **Базовые потребности**: автономия, компетентность, социальная принадлежность
    - **Внешние агенты**: тренер, родители, групповой климат, стимулы
    - **Оценка и коррекция**: анализ данных, обратная связь
    - **Этапы формирования мотивации**: вовлечение → стабилизация → углубление
    """)

# Подвал
st.markdown("---")
st.markdown("🎓 Модель формирования мотивации спортсменов к УТЗ на этапе спортивной специализации")
