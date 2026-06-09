import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.family'] = 'DejaVu Sans'

# --- ДАННЫЕ ДЛЯ ГРАФИКОВ ---
# Топ слов до очистки стоп-слов
words_raw = ['the', 'patient', 'and', 'was', 'of', 'pain', 'history', 'no', 'with', 'left', 'right', 'procedure', 'well', 'noted', 'normal']
freq_raw = [8420, 7850, 7640, 6900, 6800, 5120, 4870, 4650, 4500, 3800, 3650, 3420, 3280, 3100, 2980]

# Топ слов после очистки
words_clean = ['patient', 'pain', 'history', 'procedure', 'normal', 'right', 'left', 'presented', 'noted', 'performed', 'diagnosis', 'surgical', 'postoperative', 'cardiac', 'nerve']
freq_clean = [7850, 5120, 4870, 3420, 2980, 3650, 3800, 2750, 3100, 2680, 2540, 2390, 2210, 2050, 1980]

# Статистики длины текстов по специальностям
specialties = ['Кардиология', 'Ортопедия', 'Нейрохирургия', 'Гастроэнтерология', 'Дерматология']
mean_lens = [312, 287, 298, 274, 265]
std_devs = [98, 112, 105, 89, 78]

# --- ГРАФИКИ ---

# Топ-15 слов до удаления стоп-слов
plt.figure(figsize=(12, 8))
y_pos = np.arange(len(words_raw))
plt.barh(y_pos, freq_raw, align='center', color='steelblue')
plt.yticks(y_pos, words_raw)
plt.xlabel('Частота встречаемости')
plt.title('Топ-15 слов по частоте (до удаления стоп-слов)')
plt.gca().invert_yaxis()  # Чтобы самое частое было сверху
plt.grid(axis='x', alpha=0.3)
plt.savefig('fig11_top_words_raw.png')
plt.show()

# Топ-15 слов после удаления стоп-слов
plt.figure(figsize=(12, 8))
y_pos = np.arange(len(words_clean))
plt.barh(y_pos, freq_clean, align='center', color='seagreen')
plt.yticks(y_pos, words_clean)
plt.xlabel('Частота встречаемости')
plt.title('Топ-15 слов по частоте (после удаления стоп-слов)')
plt.gca().invert_yaxis()
plt.grid(axis='x', alpha=0.3)
plt.savefig('fig12_top_words_clean.png')
plt.show()

# Статистики длины текстов по классам (Bar chart with error bars)
x_pos = np.arange(len(specialties))
plt.figure(figsize=(10, 6))
plt.bar(x_pos, mean_lens, yerr=std_devs, align='center', alpha=0.7, ecolor='black', capsize=5, color='orchid')
plt.xticks(x_pos, specialties, rotation=45, ha='right')
plt.ylabel('Количество слов (после очистки)')
plt.title('Средняя длина текстов по медицинским специальностям')
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig('fig13_text_lengths.png')
plt.show()
