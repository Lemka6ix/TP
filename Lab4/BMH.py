import os

# text (str): строка, в которой осуществляется поиск
# pattern (str): подстрока, которую нужно найти
  
# list: список позиций, где найдена подстрока

def bmh_search(text, pattern):

    occurrences = []
    n = len(text)
    m = len(pattern)
    
    # Если подстрока пустая или длиннее текста
    if m == 0 or m > n:
        return occurrences
    
    # Построение таблицы смещений
    offset_table = {}
    for i in range(m - 1):
        offset_table[pattern[i]] = m - i - 1
    default_offset = m
    
    # Поиск подстроки
    i = 0
    while i <= n - m:
        j = m - 1  # начинаем сравнение с конца подстроки
        
        # Сравниваем символы с конца к началу
        while j >= 0 and pattern[j] == text[i + j]:
            j -= 1
        
        # Если вся подстрока совпала
        if j < 0:
            occurrences.append(i)
            i += 1  # смещаемся на 1 для поиска следующего вхождения
        else:
            # Получаем смещение из таблицы для символа в тексте
            current_char = text[i + m - 1]
            shift = offset_table.get(current_char, default_offset)
            i += shift
    
    return occurrences

def main():
    log_file = '/var/log/Xorg.0.log'
    level = input("Введите уровень журналирования (II/WW/EE/--/!!): ").strip()
    pattern = f"({level})"
    
    if not os.path.exists(log_file):
        print(f"Файл {log_file} не найден")
        return
    
    try:
        with open(log_file, 'r', encoding='utf-8', errors='ignore') as file:
            lines = file.readlines()
    except PermissionError:
        print("Недостаточно прав для чтения файла")
        return
    
    found_count = 0
    for line_num, line in enumerate(lines, 1):
        if bmh_search(line, pattern):
            print(f"Строка {line_num}: {line.strip()}")
            found_count += 1
    
    print(f"\nНайдено сообщений: {found_count}")

if __name__ == "__main__":
    main()