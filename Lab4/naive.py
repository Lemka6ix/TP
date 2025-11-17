import os

#  text (str): строка, в которой осуществляется поиск
#  pattern (str): подстрока, которую нужно найти

#  list: список позиций, где найдена подстрока

def naive_search(text, pattern):

    occurrences = []
    n = len(text)
    m = len(pattern)
    
    # Если подстрока пустая или длиннее текста
    if m == 0 or m > n:
        return occurrences
    
    # Проверяем все возможные начальные позиции
    for i in range(n - m + 1):
        match = True
        # Проверяем символы подстроки
        for j in range(m):
            if text[i + j] != pattern[j]:
                match = False
                break
        if match:
            occurrences.append(i)
    
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
        if naive_search(line, pattern):
            print(f"Строка {line_num}: {line.strip()}")
            found_count += 1
    
    print(f"\nНайдено сообщений: {found_count}")

if __name__ == "__main__":
    main()