# test_compression.py
import os
import sys
from lab5 import VitterCompressor, MTFEncoder

def test_mtf():
    """Тестирование MTF кодирования/декодирования"""
    print("=" * 50)
    print("Тестирование MTF (Move-To-Front)")
    print("=" * 50)
    
    mtf = MTFEncoder()
    
    # Тест 1: Простая строка
    test_data = b"banana"
    encoded = mtf.encode(test_data)
    print(f"Исходные данные: {list(test_data)}")
    print(f"После MTF: {list(encoded)}")
    
    # Декодирование
    mtf2 = MTFEncoder()  # Новая копия для декодирования
    decoded = mtf2.decode(encoded)
    print(f"После обратного MTF: {list(decoded)}")
    print(f"Совпадение: {test_data == decoded}")
    print()
    
    # Тест 2: Данные с повторами
    test_data = b"abracadabra"
    encoded = mtf.encode(test_data)
    print(f"Исходные: 'abracadabra'")
    print(f"MTF коды: {list(encoded)}")
    print(f"Декодировано: {mtf2.decode(encoded)}")
    print()

def test_adaptive_huffman():
    """Тестирование адаптивного Хаффмана"""
    print("=" * 50)
    print("Тестирование адаптивного Хаффмана")
    print("=" * 50)
    
    # Создаем временные файлы
    import tempfile
    
    test_strings = [
        b"banana",
        b"abracadabra",
        b"Hello, World!",
        b"Xorg log test data with (II) and (WW) tags",
        b"Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
    ]
    
    for i, test_data in enumerate(test_strings, 1):
        print(f"\nТест {i}: '{test_data[:30]}...'")
        
        # Создаем временные файлы
        with tempfile.NamedTemporaryFile(delete=False, suffix='.txt') as tmp_input:
            input_file = tmp_input.name
            tmp_input.write(test_data)
        
        with tempfile.NamedTemporaryFile(delete=False, suffix='.bin') as tmp_comp:
            comp_file = tmp_comp.name
        
        with tempfile.NamedTemporaryFile(delete=False, suffix='.txt') as tmp_decomp:
            decomp_file = tmp_decomp.name
        
        try:
            # Сжимаем и распаковываем
            compressor = VitterCompressor()
            compressor.compress(input_file, comp_file)
            compressor.decompress(comp_file, decomp_file)
            
            # Читаем результат
            with open(decomp_file, 'rb') as f:
                result = f.read()
            
            # Проверяем
            if test_data == result:
                print("✓ Успешно: данные восстановлены без потерь")
                
                # Вычисляем сжатие
                original_size = len(test_data)
                compressed_size = os.path.getsize(comp_file)
                
                if original_size > 0:
                    compression_ratio = (1 - compressed_size / original_size) * 100
                    print(f"  Размер: {original_size} → {compressed_size} байт")
                    print(f"  Сжатие: {compression_ratio:.1f}%")
                else:
                    print(f"  Размер: 0 байт")
                    
            else:
                print("✗ Ошибка: данные не совпадают")
                print(f"  Ожидалось: {test_data}")
                print(f"  Получено: {result}")
                
        finally:
            # Удаляем временные файлы
            for f in [input_file, comp_file, decomp_file]:
                try:
                    os.unlink(f)
                except:
                    pass

def test_file_compression():
    """Тестирование сжатия файла"""
    print("=" * 50)
    print("Тестирование сжатия файла")
    print("=" * 50)
    
    # Создаем тестовый файл с данными, похожими на Xorg лог
    test_log_content = """[     5.123] (II) Loading extension GLX
[     5.124] (II) Loading extension DRI2
[     5.125] (II) Loading extension DRI3
[     5.126] (WW) Warning: Failed to load module "nouveau"
[     5.127] (II) UnloadModule: "nouveau"
[     5.128] (II) Unloading nouveau
[     5.129] (EE) Error: Module does not exist
[     5.130] (II) LoadModule: "modesetting"
[     5.131] (II) Loading /usr/lib/xorg/modules/drivers/modesetting_drv.so
[     5.132] (II) Module modesetting: vendor="X.Org Foundation"
"""
    
    import tempfile
    
    # Создаем временные файлы
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.log', encoding='utf-8') as tmp_input:
        input_file = tmp_input.name
        tmp_input.write(test_log_content)
    
    with tempfile.NamedTemporaryFile(delete=False, suffix='.bin') as tmp_comp:
        comp_file = tmp_comp.name
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.log', encoding='utf-8') as tmp_decomp:
        decomp_file = tmp_decomp.name
    
    try:
        print(f"Исходный файл: {input_file}")
        print(f"Размер: {os.path.getsize(input_file)} байт")
        
        # Сжимаем
        compressor = VitterCompressor()
        compressor.compress(input_file, comp_file)
        
        compressed_size = os.path.getsize(comp_file)
        print(f"\nСжатый файл: {comp_file}")
        print(f"Размер: {compressed_size} байт")
        
        # Вычисляем степень сжатия
        original_size = os.path.getsize(input_file)
        if original_size > 0:
            ssr = (1 - compressed_size / original_size) * 100
            print(f"\nСтепень сжатия (SSR): {ssr:.2f}%")
        
        # Распаковываем
        compressor.decompress(comp_file, decomp_file)
        
        # Сравниваем файлы
        with open(input_file, 'r', encoding='utf-8') as f1, \
             open(decomp_file, 'r', encoding='utf-8') as f2:
            content1 = f1.read()
            content2 = f2.read()
        
        if content1 == content2:
            print("\n✓ Файлы идентичны после распаковки")
        else:
            print("\n✗ Файлы различаются после распаковки")
            
            # Показываем различия
            import difflib
            diff = list(difflib.unified_diff(
                content1.splitlines(),
                content2.splitlines(),
                lineterm=''
            ))
            for line in diff[:5]:
                print(f"  {line}")
            if len(diff) > 5:
                print(f"  ... и еще {len(diff) - 5} различий")
                
    finally:
        # Удаляем временные файлы
        for f in [input_file, comp_file, decomp_file]:
            try:
                os.unlink(f)
            except:
                pass

def run_all_tests():
    """Запуск всех тестов"""
    print("Начало тестирования архиватора MTF + Адаптивный Хаффман")
    print()
    
    test_mtf()
    test_adaptive_huffman()
    test_file_compression()
    
    print("\n" + "=" * 50)
    print("Все тесты завершены")
    print("=" * 50)

if __name__ == "__main__":
    run_all_tests()