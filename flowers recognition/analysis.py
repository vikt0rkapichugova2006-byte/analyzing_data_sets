import os
import random
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import urllib.request
import tarfile
import shutil

plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['font.size'] = 12

DATA_DIR = 'data'
TRAIN_DIR = os.path.join(DATA_DIR, 'train')

CLASS_NAMES = ['rose', 'sunflower']
RUSSIAN_NAMES = {'rose': 'Роза', 'sunflower': 'Подсолнух'}

def download_dataset():
    """Загружает датасет Flowers Recognition"""
    print("📥 Загрузка датасета Flowers Recognition...")
    
    # Удаляем старые данные если есть
    if os.path.exists(DATA_DIR):
        shutil.rmtree(DATA_DIR)
    
    os.makedirs(TRAIN_DIR, exist_ok=True)
    
    # Источник: TensorFlow flowers dataset (надёжная прямая ссылка)
    url = "https://storage.googleapis.com/download.tensorflow.org/example_images/flower_photos.tgz"
    tar_path = os.path.join(DATA_DIR, 'flower_photos.tgz')
    
    try:
        print("Загрузка файла (может занять 1-2 минуты)...")
        urllib.request.urlretrieve(url, tar_path)
        print(f"✓ Файл загружен: {os.path.getsize(tar_path) / 1024 / 1024:.1f} МБ")
        
        print("Распаковка...")
        with tarfile.open(tar_path, 'r:gz') as tar:
            tar.extractall(DATA_DIR)
        
        extracted_dir = os.path.join(DATA_DIR, 'flower_photos')
        
        # Маппинг папок
        folder_map = {
            'roses': 'rose',
            'sunflowers': 'sunflower'
        }
        
        success = True
        for src_name, dst_name in folder_map.items():
            src_dir = os.path.join(extracted_dir, src_name)
            dst_dir = os.path.join(TRAIN_DIR, dst_name)
            
            if os.path.exists(src_dir):
                # Считаем файлы ДО копирования
                n_files = len([f for f in os.listdir(src_dir) 
                              if f.lower().endswith(('.jpg', '.jpeg', '.png'))])
                
                if n_files < 100:
                    print(f" Папка {src_name} содержит только {n_files} изображений (ожидалось ~700+)")
                    success = False
                
                shutil.copytree(src_dir, dst_dir)
                print(f"✓ {src_name} → {dst_name}: {n_files} изображений")
            else:
                print(f" Папка {src_name} не найдена в архиве!")
                success = False
        
        # Удаляем временные файлы
        shutil.rmtree(extracted_dir)
        os.remove(tar_path)
        
        if success:
            print("\n Датасет успешно загружен!")
            return True
        else:
            print("\n️ Датасет загружен неполностью!")
            return False
            
    except Exception as e:
        print(f" Ошибка при загрузке: {e}")
        return False

need_download = False

if not os.path.exists(TRAIN_DIR):
    print(" Папка data/train не найдена")
    need_download = True
else:
    # Проверяем наличие обеих папок
    missing_classes = []
    for class_name in CLASS_NAMES:
        class_dir = os.path.join(TRAIN_DIR, class_name)
        if not os.path.exists(class_dir):
            missing_classes.append(class_name)
        else:
            n_files = len([f for f in os.listdir(class_dir) 
                          if f.lower().endswith(('.jpg', '.jpeg', '.png'))])
            print(f"✓ Класс '{class_name}': {n_files} изображений")
            if n_files < 100:
                print(f"  Мало изображений (ожидалось 700+)")
    
    if missing_classes:
        print(f"\n Отсутствуют папки: {missing_classes}")
        need_download = True

if need_download:
    print("\n" + "="*60)
    print("НУЖНА ЗАГРУЗКА ДАТАСЕТА")
    print("="*60)
    success = download_dataset()
    
    if not success:
        print("\n" + "="*60)
        print("АЛЬТЕРНАТИВНЫЙ СПОСОБ: Kaggle API")
        print("="*60)
        print("Если загрузка не удалась, попробуйте через Kaggle:")
        print("\n1. Установите kaggle:")
        print("   pip install kaggle")
        print("\n2. Скачайте датасет:")
        print("   kaggle datasets download -d alxmamaev/flowers-recognition")
        print("\n3. Распакуйте:")
        print("   unzip flowers-recognition.zip -d data/")
        print("\n4. Создайте структуру:")
        print("   mkdir -p data/train")
        print("   mv data/flowers/rose data/train/")
        print("   mv data/flowers/sunflower data/train/")
        print("\nИли скачайте вручную с:")
        print("https://www.kaggle.com/datasets/alxmamaev/flowers-recognition")
        exit()

image_info = {}
for class_name in CLASS_NAMES:
    class_dir = os.path.join(TRAIN_DIR, class_name)
    
    if not os.path.exists(class_dir):
        print(f" КРИТИЧЕСКАЯ ОШИБКА: Папка '{class_name}' не найдена!")
        print(f"   Ожидаемый путь: {class_dir}")
        exit()
    
    files = [f for f in os.listdir(class_dir) 
             if f.lower().endswith(('.jpg', '.jpeg', '.png', '.JPG', '.JPEG', '.PNG'))]
    
    if len(files) == 0:
        print(f" Папка '{class_name}' пуста!")
        exit()
    
    sizes = []
    valid_files = []
    
    for fname in files:
        fpath = os.path.join(class_dir, fname)
        try:
            with Image.open(fpath) as img:
                w, h = img.size
                sizes.append((w, h))
                valid_files.append(fname)
        except Exception as e:
            print(f" Не удалось открыть {fname}: {e}")
    
    image_info[class_name] = {
        'count': len(valid_files),
        'sizes': sizes,
        'files': valid_files
    }
    print(f" Класс '{class_name}': {len(valid_files)} изображений")

print("\n" + "="*60)
print("ГЕНЕРАЦИЯ ГРАФИКОВ...")
print("="*60)

fig, ax = plt.subplots(figsize=(8, 5))

counts = [image_info[c]['count'] for c in CLASS_NAMES]
colors = ['#E74C3C', '#F1C40F']

bars = ax.bar([RUSSIAN_NAMES[c] for c in CLASS_NAMES], counts, 
              color=colors, edgecolor='black', alpha=0.9, width=0.6)

for bar, count in zip(bars, counts):
    ax.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 10, 
            str(count), ha='center', va='bottom', fontsize=14, fontweight='bold')

total = sum(counts)
percentages = [f"{c/total*100:.1f}%" for c in counts]
ax.set_xticklabels([f"{RUSSIAN_NAMES[c]}\n({p})" for c, p in zip(CLASS_NAMES, percentages)])

ax.set_title('Рисунок 3.1 — Распределение классов в выборке', fontsize=14, fontweight='bold', pad=15)
ax.set_ylabel('Количество изображений', fontsize=12)
ax.grid(axis='y', alpha=0.3, linestyle='--')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.set_ylim(0, max(counts) * 1.15)

plt.tight_layout()
plt.savefig('рис_3_1_распределение_классов.png', bbox_inches='tight', dpi=300)
plt.show()
print("✓ Сохранён: рис_3_1_распределение_классов.png")

n_examples = 5
fig, axes = plt.subplots(2, n_examples, figsize=(16, 7))
fig.suptitle('Рисунок 3.2 — Примеры изображений из выборки', 
             fontsize=14, fontweight='bold', y=0.98)

for row_idx, class_name in enumerate(CLASS_NAMES):
    files = image_info[class_name]['files']
    n_to_show = min(n_examples, len(files))
    selected = random.sample(files, n_to_show)
    
    for col_idx, fname in enumerate(selected):
        fpath = os.path.join(TRAIN_DIR, class_name, fname)
        try:
            img = Image.open(fpath)
            axes[row_idx, col_idx].imshow(img)
        except:
            axes[row_idx, col_idx].text(0.5, 0.5, 'Error', ha='center', va='center')
        
        axes[row_idx, col_idx].set_title(f'{RUSSIAN_NAMES[class_name]} #{col_idx+1}', fontsize=10)
        axes[row_idx, col_idx].axis('off')
    
    for col_idx in range(n_to_show, n_examples):
        axes[row_idx, col_idx].axis('off')

plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.savefig('рис_3_2_примеры_изображений.png', bbox_inches='tight', dpi=300)
plt.show()
print("✓ Сохранён: рис_3_2_примеры_изображений.png")

all_widths = []
all_heights = []
for class_name in CLASS_NAMES:
    for w, h in image_info[class_name]['sizes']:
        all_widths.append(w)
        all_heights.append(h)

fig, axes = plt.subplots(1, 3, figsize=(18, 5))
fig.suptitle('Рисунок 3.3 — Распределение размеров изображений в выборке', 
             fontsize=14, fontweight='bold')

axes[0].hist(all_widths, bins=30, color='#3498DB', edgecolor='white', alpha=0.8)
axes[0].axvline(np.mean(all_widths), color='red', linestyle='--', 
               linewidth=2, label=f'Среднее: {np.mean(all_widths):.0f}')
axes[0].set_title('Ширина изображений', fontsize=12, fontweight='bold')
axes[0].set_xlabel('Ширина (px)', fontsize=11)
axes[0].set_ylabel('Частота', fontsize=11)
axes[0].legend(fontsize=10)
axes[0].grid(axis='y', alpha=0.3)

axes[1].hist(all_heights, bins=30, color='#2ECC71', edgecolor='white', alpha=0.8)
axes[1].axvline(np.mean(all_heights), color='red', linestyle='--', 
               linewidth=2, label=f'Среднее: {np.mean(all_heights):.0f}')
axes[1].set_title('Высота изображений', fontsize=12, fontweight='bold')
axes[1].set_xlabel('Высота (px)', fontsize=11)
axes[1].set_ylabel('Частота', fontsize=11)
axes[1].legend(fontsize=10)
axes[1].grid(axis='y', alpha=0.3)

aspect_ratios = [w/h for w, h in zip(all_widths, all_heights)]
axes[2].scatter(range(len(aspect_ratios)), sorted(aspect_ratios), 
               color='#9B59B6', alpha=0.5, s=10)
axes[2].axhline(np.mean(aspect_ratios), color='red', linestyle='--', 
               linewidth=2, label=f'Среднее: {np.mean(aspect_ratios):.2f}')
axes[2].set_title('Соотношение сторон (ширина/высота)', fontsize=12, fontweight='bold')
axes[2].set_xlabel('Индекс изображения', fontsize=11)
axes[2].set_ylabel('Соотношение сторон', fontsize=11)
axes[2].legend(fontsize=10)
axes[2].grid(alpha=0.3)

plt.tight_layout()
plt.savefig('рис_3_3_распределение_размеров.png', bbox_inches='tight', dpi=300)
plt.show()
print("✓ Сохранён: рис_3_3_распределение_размеров.png")

print("\n" + "="*60)
print("СТАТИСТИКА ДАТАСЕТА")
print("="*60)

widths_arr = np.array(all_widths)
heights_arr = np.array(all_heights)
ratios_arr = np.array(aspect_ratios)

print(f"\nОбщее количество изображений: {len(all_widths)}")
for class_name in CLASS_NAMES:
    print(f"  {RUSSIAN_NAMES[class_name]}: {image_info[class_name]['count']}")

print(f"\nРазмеры изображений:")
print(f"  Ширина: min={int(widths_arr.min())}, max={int(widths_arr.max())}, mean={widths_arr.mean():.1f}")
print(f"  Высота: min={int(heights_arr.min())}, max={int(heights_arr.max())}, mean={heights_arr.mean():.1f}")
print(f"  Соотношение сторон: min={ratios_arr.min():.2f}, max={ratios_arr.max():.2f}, mean={ratios_arr.mean():.2f}")

small_images = sum(1 for w in all_widths if w < 200)
vertical_images = sum(1 for r in aspect_ratios if r < 0.6)

print(f"\n Проблемные изображения:")
print(f"  С шириной < 200px: {small_images} ({small_images/len(all_widths)*100:.1f}%)")
print(f"  Вертикальные кадры (соотн. < 0.6): {vertical_images} ({vertical_images/len(aspect_ratios)*100:.1f}%)")

print("\n" + "="*60)
print("ВСЕ ГРАФИКИ УСПЕШНО СОХРАНЕНЫ!")
print("="*60)
