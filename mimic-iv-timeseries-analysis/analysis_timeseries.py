import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.unicode_minus'] = False

# --- ГЕНЕРАЦИЯ ДАННЫХ ВРЕМЕННЫХ РЯДОВ ---
hours = np.arange(0, 72, 1) # 72 часа
# Симуляция параметров с шумом и трендами
heart_rate = 80 + 10 * np.sin(hours / 10) + np.random.normal(0, 5, len(hours))
sys_bp = 120 + 5 * np.sin(hours / 12) + np.random.normal(0, 8, len(hours))
dia_bp = sys_bp * 0.6 + np.random.normal(0, 3, len(hours))
temp = 36.6 + 0.5 * np.sin(hours / 24) + np.random.normal(0, 0.2, len(hours))
spo2 = 97 - np.abs(np.random.normal(0, 1, len(hours)))
resp_rate = 18 + 2 * np.sin(hours / 15) + np.random.normal(0, 2, len(hours))

# Создание DataFrame
ts_data = pd.DataFrame({
    'Час': hours,
    'ЧСС': heart_rate,
    'САД': sys_bp,
    'ДАД': dia_bp,
    'Температура': temp,
    'SpO2': spo2,
    'ЧДД': resp_rate
})

# --- ГРАФИКИ ---

# Графики шести каналов временного ряда
fig, axs = plt.subplots(6, 1, figsize=(14, 12), sharex=True)
channels = ['ЧСС', 'САД', 'ДАД', 'Температура', 'SpO2', 'ЧДД']
colors = ['b', 'g', 'r', 'c', 'm', 'y']

for i, ch in enumerate(channels):
    axs[i].plot(ts_data['Час'], ts_data[ch], color=colors[i], linewidth=1)
    axs[i].set_ylabel(ch)
    axs[i].grid(True, linestyle='--', alpha=0.5)
    axs[i].set_title(f'Динамика показателя: {ch}')

axs[-1].set_xlabel('Время (часы)')
plt.suptitle('Графики физиологических параметров пациента (MIMIC-IV)', fontsize=16)
plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.savefig('fig12_ts_channels.png')
plt.show()

# Сравнение диапазонов значений всех каналов (Boxplot)
plt.figure(figsize=(12, 6))
bp = plt.boxplot([ts_data[ch].values for ch in channels], labels=channels, patch_artist=True)
colors_box = ['lightblue', 'lightgreen', 'lightcoral', 'gold', 'plum', 'lightyellow']
for patch, color in zip(bp['boxes'], colors_box):
    patch.set_facecolor(color)
plt.title('Сравнение диапазонов значений каналов (Boxplot)')
plt.ylabel('Значение')
plt.grid(True, axis='y', alpha=0.3)
plt.savefig('fig14_ts_ranges.png')
plt.show()

# Корреляция между каналами (Scatter Plot Matrix style or specific pairs)
# Покажем связь САД и ДАД, а также ЧСС и ЧДД
fig, axs = plt.subplots(1, 2, figsize=(14, 6))

# САД vs ДАД
axs[0].scatter(ts_data['САД'], ts_data['ДАД'], c='blue', alpha=0.5, s=10)
axs[0].set_title('Корреляция: САД и ДАД')
axs[0].set_xlabel('Систолическое АД')
axs[0].set_ylabel('Диастолическое АД')

# ЧСС vs ЧДД
axs[1].scatter(ts_data['ЧСС'], ts_data['ЧДД'], c='red', alpha=0.5, s=10)
axs[1].set_title('Корреляция: ЧСС и ЧДД')
axs[1].set_xlabel('ЧСС (уд/мин)')
axs[1].set_ylabel('ЧДД (вд/мин)')

plt.suptitle('Корреляционные зависимости между параметрами')
plt.tight_layout()
plt.savefig('fig15_ts_correlations.png')
plt.show()

# Дополнительный рисунок: Анализ пропусков (симуляция)
# Создадим маску пропусков
missing_mask = np.random.rand(len(hours)) < 0.08 # 8% пропусков
ts_data_missing = ts_data.copy()
ts_data_missing.loc[missing_mask, 'Температура'] = np.nan

plt.figure(figsize=(12, 4))
plt.plot(ts_data_missing['Час'], ts_data_missing['Температура'], 'o-', markersize=3, label='Измерения')
plt.title('Пример пропусков в данных (Температура тела)')
plt.xlabel('Время (часы)')
plt.ylabel('Температура (°C)')
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig('fig_ts_missing_example.png')
plt.show()
