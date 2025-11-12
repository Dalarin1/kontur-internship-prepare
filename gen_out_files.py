import os
import subprocess
import sys

def parse_test_file(input_file_path):
    """
    Парсит .in файл и возвращает список тестов
    """
    tests = {}
    
    with open(input_file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Разделяем на тесты по @test-
    test_blocks = content.split('@')
    
    for block in test_blocks:
        if not block.strip() or not block.startswith('test-'):
            continue
            
        # Извлекаем ID теста и данные
        lines = block.strip().split('\n')
        test_id = lines[0].strip()
        test_data = '\n'.join(lines[1:]).strip()
        
        tests[test_id] = test_data
    
    return tests

def run_tests_on_exe(exe_path, input_file_path, output_file_path):
    """
    Запускает тесты на исполняемом файле и генерирует .out файл
    """
    tests = parse_test_file(input_file_path)
    results = {}
    
    print(f"Запуск тестов из {input_file_path} на {exe_path}")
    
    for test_id, test_data in tests.items():
        print(f"Обработка {test_id}...")
        
        try:
            # Запускаем процесс и передаем входные данные
            process = subprocess.Popen(
                [exe_path],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Передаем данные и получаем результат
            stdout, stderr = process.communicate(input=test_data, timeout=30)
            
            if process.returncode != 0:
                print(f"  Ошибка в {test_id}: код возврата {process.returncode}")
                if stderr:
                    print(f"  Stderr: {stderr}")
                results[test_id] = f"ERROR: return code {process.returncode}"
            else:
                results[test_id] = stdout.strip()
                
        except subprocess.TimeoutExpired:
            print(f"  Таймаут в {test_id}")
            results[test_id] = "ERROR: timeout"
        except Exception as e:
            print(f"  Исключение в {test_id}: {e}")
            results[test_id] = f"ERROR: {str(e)}"
    
    # Записываем результаты в .out файл
    with open(output_file_path, 'w', encoding='utf-8') as f:
        for test_id, result in results.items():
            f.write(f"@{test_id}\n")
            f.write(f"{result}\n")
    
    print(f"Результаты записаны в {output_file_path}")
    return results

def main():
    if len(sys.argv) != 4:
        print("Использование: python generate_out.py <exe_file> <input_file.in> <output_file.out>")
        print("Пример: python generate_out.py jury_solution.exe winter-2025-a.in winter-2025-a.out")
        sys.exit(1)
    
    exe_path = sys.argv[1]
    input_file = sys.argv[2]
    output_file = sys.argv[3]
    
    if not os.path.exists(exe_path):
        print(f"Ошибка: файл {exe_path} не найден")
        sys.exit(1)
    
    if not os.path.exists(input_file):
        print(f"Ошибка: файл {input_file} не найден")
        sys.exit(1)
    
    run_tests_on_exe(exe_path, input_file, output_file)

if __name__ == "__main__":

    # TEST_DIR = os.path.join(os.getcwd(), "test")
    # curdir = os.path.join(TEST_DIR, "summer-2025")
    
    # for filename in 'abcde':
    #     run_tests_on_exe(
    #         os.path.join(curdir, filename + '.exe'),
    #         os.path.join(curdir, filename + '.in'),
    #         os.path.join(curdir, filename + '.out')
    #     )
    main()