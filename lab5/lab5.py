import sys
import os
import difflib

class MTFEncoder:
    """Кодирование Move-To-Front"""
    def __init__(self):
        self.alphabet = list(range(256))
    
    def encode(self, data):
        """Кодирование MTF"""
        result = []
        for byte in data:
            idx = self.alphabet.index(byte)
            result.append(idx)
            self.alphabet.pop(idx)
            self.alphabet.insert(0, byte)
        return bytes(result)
    
    def decode(self, data):
        """Декодирование MTF"""
        result = []
        for idx in data:
            byte = self.alphabet[idx]
            result.append(byte)
            self.alphabet.pop(idx)
            self.alphabet.insert(0, byte)
        return bytes(result)

class VitterNode:
    """Узел Виттера"""
    def __init__(self, weight=0, symbol=None, parent=None):
        self.weight = weight
        self.symbol = symbol
        self.parent = parent
        self.left = None
        self.right = None
        self.order = 0
    
    def is_leaf(self):
        return self.left is None and self.right is None
    
    def is_nyt(self):
        return self.symbol is None and self.weight == 0

class Vitter:
    """Виттер с NYT"""
    def __init__(self):
        self.nyt = VitterNode(weight=0, symbol=None) 
        self.nyt.order = 1000
        self.root = self.nyt
        self.symbol_nodes = {}
        self.nodes_list = [self.nyt]
        self.order_counter = 999
    
    def find_node_by_symbol(self, symbol, node=None):
        """Найти узел по символу"""
        if node is None:
            node = self.root
        
        if node.is_leaf() and node.symbol == symbol:
            return node
        
        result = None
        if node.left:
            result = self.find_node_by_symbol(symbol, node.left)
        if not result and node.right:
            result = self.find_node_by_symbol(symbol, node.right)
        
        return result
    
    def get_code(self, symbol):
        """Получить код для символа"""
        node = self.find_node_by_symbol(symbol)
        if node is None:
            return None
        
        code = []
        current = node
        while current.parent:
            parent = current.parent
            if parent.left == current:
                code.append(0)
            else:
                code.append(1)
            current = parent
        
        return list(reversed(code))
    
    def get_nyt_code(self):
        """Получить код для NYT узла"""
        code = []
        node = self.nyt
        while node.parent:
            parent = node.parent
            if parent.left == node:
                code.append(0)
            else:
                code.append(1)
            node = parent
        
        return list(reversed(code))
    
    def update_tree(self, symbol):
        """Обновить дерево после появления символа"""
        if symbol in self.symbol_nodes:
            node = self.symbol_nodes[symbol]
            self.update_existing_symbol(node)
        else:
            self.add_new_symbol(symbol)
    
    def update_existing_symbol(self, node):
        """Обновить существующий символ"""
        # Найти блок с таким же весом и максимальным порядком
        block_nodes = [n for n in self.nodes_list if n.weight == node.weight]
        if block_nodes:
            max_order_node = max(block_nodes, key=lambda n: n.order)
            if max_order_node != node:
                self.swap_nodes(node, max_order_node)
        
        node.weight += 1
        
        # Поднимаемся вверх по дереву
        current = node.parent
        while current:
            block_nodes = [n for n in self.nodes_list if n.weight == current.weight]
            if block_nodes:
                max_order_node = max(block_nodes, key=lambda n: n.order)
                if max_order_node != current:
                    self.swap_nodes(current, max_order_node)
            
            current.weight += 1
            current = current.parent
    
    def add_new_symbol(self, symbol):
        """Добавить новый символ"""
        # Создаем новый внутренний узел на месте NYT
        new_internal = VitterNode(weight=1, symbol=None, parent=self.nyt.parent) 
        new_internal.order = self.order_counter
        self.order_counter -= 1
        
        # Создаем новый лист для символа
        new_leaf = VitterNode(weight=1, symbol=symbol, parent=new_internal) 
        new_leaf.order = self.order_counter
        self.order_counter -= 1
        
        # Обновляем связи
        if self.nyt.parent:
            if self.nyt.parent.left == self.nyt:
                self.nyt.parent.left = new_internal
            else:
                self.nyt.parent.right = new_internal
        else:
            self.root = new_internal
        
        new_internal.left = self.nyt
        new_internal.right = new_leaf
        self.nyt.parent = new_internal
        
        # Добавляем в списки
        self.symbol_nodes[symbol] = new_leaf
        self.nodes_list.append(new_internal)
        self.nodes_list.append(new_leaf)
        
        # Обновляем дерево
        current = new_internal.parent
        while current:
            block_nodes = [n for n in self.nodes_list if n.weight == current.weight]
            if block_nodes:
                max_order_node = max(block_nodes, key=lambda n: n.order)
                if max_order_node != current:
                    self.swap_nodes(current, max_order_node)
            
            current.weight += 1
            current = current.parent
    
    def swap_nodes(self, node1, node2):
        """Поменять узлы местами"""
        if node1 == node2 or not node1.parent or not node2.parent:
            return
        
        # Меняем местами в родителях
        parent1 = node1.parent
        parent2 = node2.parent
        
        if parent1.left == node1:
            parent1.left = node2
        else:
            parent1.right = node2
        
        if parent2.left == node2:
            parent2.left = node1
        else:
            parent2.right = node1
        
        # Меняем родителей
        node1.parent, node2.parent = parent2, parent1
        
        # Меняем порядок
        node1.order, node2.order = node2.order, node1.order

class VitterEncoder: 
    """Кодировщик Виттера"""
    def __init__(self):
        self.tree = Vitter()
        self.bit_buffer = 0
        self.bit_count = 0
    
    def encode_symbol(self, symbol, output_stream):
        """Закодировать один символ"""
        code = self.tree.get_code(symbol)
        
        if code is None:
            # Новый символ
            nyt_code = self.tree.get_nyt_code()
            for bit in nyt_code:
                self.output_bit(bit, output_stream)
            
            # ASCII код символа (8 бит)
            for i in range(7, -1, -1):
                bit = (symbol >> i) & 1
                self.output_bit(bit, output_stream)
        else:
            # Существующий символ
            for bit in code:
                self.output_bit(bit, output_stream)
        
        self.tree.update_tree(symbol)
    
    def output_bit(self, bit, output_stream):
        """Вывести бит в поток"""
        self.bit_buffer = (self.bit_buffer << 1) | bit
        self.bit_count += 1
        
        if self.bit_count == 8:
            output_stream.write(bytes([self.bit_buffer]))
            self.bit_buffer = 0
            self.bit_count = 0
    
    def flush(self, output_stream):
        """Завершить кодирование"""
        # Маркер конца файла
        nyt_code = self.tree.get_nyt_code()
        for bit in nyt_code:
            self.output_bit(bit, output_stream)
        
        # Специальный символ 255
        for i in range(7, -1, -1):
            bit = (255 >> i) & 1
            self.output_bit(bit, output_stream)
        
        if self.bit_count > 0:
            self.bit_buffer <<= (8 - self.bit_count)
            output_stream.write(bytes([self.bit_buffer]))

class VitterDecoder:
    """Декодировщик Виттера"""
    def __init__(self):
        self.tree = Vitter() 
        self.bit_buffer = 0
        self.bit_count = 0
    
    def input_bit(self, input_stream):
        """Прочитать бит из потока"""
        if self.bit_count == 0:
            data = input_stream.read(1)
            if not data:
                return -1
            self.bit_buffer = data[0]
            self.bit_count = 8
        
        self.bit_count -= 1
        bit = (self.bit_buffer >> self.bit_count) & 1
        return bit
    
    def decode_symbol(self, input_stream):
        """Декодировать один символ"""
        node = self.tree.root
        
        while not node.is_leaf():
            bit = self.input_bit(input_stream)
            if bit == -1:
                return 256
            
            if bit == 0:
                node = node.left
            else:
                node = node.right
        
        if node.is_nyt():
            ascii_code = 0
            for i in range(8):
                bit = self.input_bit(input_stream)
                if bit == -1:
                    return 256
                ascii_code = (ascii_code << 1) | bit
            
            if ascii_code == 255:
                return 256
            
            symbol = ascii_code
        else:
            symbol = node.symbol
        
        if symbol != 256:
            self.tree.update_tree(symbol)
        
        return symbol

class VitterCompressor:
    """Архиватор с Виттером"""
    def __init__(self):
        pass
    
    def compress(self, input_file, output_file):
        """Сжатие файла"""
        with open(input_file, 'rb') as f:
            data = f.read()
        
        if not data:
            return
        
        # MTF преобразование
        mtf = MTFEncoder()
        mtf_data = mtf.encode(data)
        
        # Адаптивное кодирование Хаффмана
        with open(output_file, 'wb') as f:
            encoder = VitterEncoder()   
            
            for byte in mtf_data:
                encoder.encode_symbol(byte, f)
            
            encoder.flush(f)
    
    def decompress(self, input_file, output_file):
        """Распаковка файла"""
        with open(input_file, 'rb') as f:
            decoder = VitterDecoder() 
            
            decoded_data = []
            while True:
                symbol = decoder.decode_symbol(f)
                if symbol == 256:
                    break
                decoded_data.append(symbol)
        
        # Обратное MTF преобразование
        mtf = MTFEncoder()
        result_data = mtf.decode(bytes(decoded_data))
        
        with open(output_file, 'wb') as f:
            f.write(result_data)

def compare_files(file1, file2):
    """Сравнение двух файлов с помощью diff"""
    with open(file1, 'r', encoding='utf-8', errors='ignore') as f1:
        with open(file2, 'r', encoding='utf-8', errors='ignore') as f2:
            diff = list(difflib.unified_diff(
                f1.readlines(),
                f2.readlines(),
                fromfile=file1,
                tofile=file2,
                lineterm=''
            ))
    
    if not diff:
        print("✓ Файлы идентичны")
        return True
    else:
        print("✗ Файлы различаются")
        for line in diff[:10]:
            print(line)
        if len(diff) > 10:
            print(f"... и еще {len(diff) - 10} различий")
        return False

def calculate_compression_ratio(original_file, compressed_file):
    """Вычисление степени сжатия"""
    original_size = os.path.getsize(original_file)
    compressed_size = os.path.getsize(compressed_file)
    
    if original_size == 0:
        return 0
    
    ssr = (1 - compressed_size / original_size) * 100
    return ssr

def main():
    """Основная функция программы"""
    if len(sys.argv) != 4:
        print("Использование:")
        print("  Сжатие: python archiver.py compress входной_файл выходной_файл")
        print("  Распаковка: python archiver.py decompress входной_файл выходной_файл")
        return
    
    command = sys.argv[1]
    input_file = sys.argv[2]
    output_file = sys.argv[3]
    
    if not os.path.exists(input_file):
        print(f"Ошибка: файл '{input_file}' не найден")
        return
    
    compressor = VitterCompressor() 
    
    try:
        if command == 'compress':
            print(f"Сжатие файла '{input_file}'...")
            original_size = os.path.getsize(input_file)
            compressor.compress(input_file, output_file)
            compressed_size = os.path.getsize(output_file)
            ssr = calculate_compression_ratio(input_file, output_file)
            
            print(f"Размер исходного файла: {original_size} байт")
            print(f"Размер сжатого файла: {compressed_size} байт")
            print(f"Степень сжатия (SSR): {ssr:.2f}%")
            
        elif command == 'decompress':
            print(f"Распаковка файла '{input_file}'...")
            compressor.decompress(input_file, output_file)
            print(f"Файл распакован в '{output_file}'")
            
            # Проверка целостности
            if command == 'compress' and os.path.exists(input_file + ".orig"):
                print(f"\nСравнение с оригиналом:")
                compare_files(input_file + ".orig", output_file)
        
        else:
            print(f"Неизвестная команда: {command}")
            
    except Exception as e:
        print(f"Ошибка: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()