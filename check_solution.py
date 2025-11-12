import os
import subprocess
import sys

def parse_out_file(out_file_path):
    """
    Парсит .out файл и возвращает ожидаемые результаты
    """
    expected_results = {}
    
    with open(out_file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Разделяем на тесты по @test-
    test_blocks = content.split('@')
    
    for block in test_blocks:
        if not block.strip() or not block.startswith('test-'):
            continue
            
        # Извлекаем ID теста и ожидаемый результат
        lines = block.strip().split('\n')
        test_id = lines[0].strip()
        expected_result = '\n'.join(lines[1:]).strip()
        
        expected_results[test_id] = expected_result
    
    return expected_results

def check_solution(candidate_exe_path, input_file_path, expected_out_file_path):
    """
    Проверяет решение кандидата на тестах
    """
    # Получаем тесты из .in файла
    tests = parse_test_file(input_file_path)
    
    # Получаем ожидаемые результаты из .out файла
    expected_results = parse_out_file(expected_out_file_path)
    
    print(f"Проверка {candidate_exe_path} на тестах из {input_file_path}")
    print("=" * 50)
    
    passed_tests = 0
    failed_tests = 0
    
    for test_id, test_data in tests.items():
        print(f"Тест {test_id}: ", end="")
        
        if test_id not in expected_results:
            print(f"СКИП - нет ожидаемого результата в .out файле")
            continue
        
        expected = expected_results[test_id]
        
        try:
            # Запускаем решение кандидата
            process = subprocess.Popen(
                [candidate_exe_path],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            stdout, stderr = process.communicate(input=test_data, timeout=30)
            actual = stdout.strip()
            
            if process.returncode != 0:
                print(f"ПРОВАЛ - код возврата {process.returncode}")
                if stderr:
                    print(f"  Stderr: {stderr}")
                failed_tests += 1
            elif actual == expected:
                print("ПРОЙДЕН")
                passed_tests += 1
            else:
                print("ПРОВАЛ")
                print(f"  Ожидалось: {expected}")
                print(f"  Получено:  {actual}")
                failed_tests += 1
                
        except subprocess.TimeoutExpired:
            print("ПРОВАЛ - таймаут")
            failed_tests += 1
        except Exception as e:
            print(f"ПРОВАЛ - исключение: {e}")
            failed_tests += 1
    
    print("=" * 50)
    print(f"Итог: {passed_tests} пройдено, {failed_tests} провалено")
    
    return passed_tests, failed_tests

def parse_test_file(input_file_path):
    """
    Парсит .in файл (такая же функция как в первом скрипте)
    """
    tests = {}
    
    with open(input_file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    test_blocks = content.split('@')
    
    for block in test_blocks:
        if not block.strip() or not block.startswith('test-'):
            continue
            
        lines = block.strip().split('\n')
        test_id = lines[0].strip()
        test_data = '\n'.join(lines[1:]).strip()
        
        tests[test_id] = test_data
    
    return tests

def main():
    if len(sys.argv) != 4:
        print("Использование: python check_solution.py <candidate_exe> <input_file.in> <expected_output_file.out>")
        print("Пример: python check_solution.py candidate_solution.exe winter-2025-a.in winter-2025-a.out")
        sys.exit(1)
    
    candidate_exe = sys.argv[1]
    input_file = sys.argv[2]
    expected_out_file = sys.argv[3]
    
    if not os.path.exists(candidate_exe):
        print(f"Ошибка: файл {candidate_exe} не найден")
        sys.exit(1)
    
    if not os.path.exists(input_file):
        print(f"Ошибка: файл {input_file} не найден")
        sys.exit(1)
    
    if not os.path.exists(expected_out_file):
        print(f"Ошибка: файл {expected_out_file} не найден")
        sys.exit(1)
    
    passed, failed = check_solution(candidate_exe, input_file, expected_out_file)
    
    # Возвращаем код выхода: 0 если все тесты прошли, иначе 1
    sys.exit(1 if failed > 0 else 0)

if __name__ == "__main__":
    main()
    # TEST_DIR = os.path.join(os.getcwd(), "test")
    # curdir = os.path.join(TEST_DIR, "winter-2024")
    
    # for filename in 'abcde':
    #     check_solution(
    #         os.path.join(curdir, filename + '.exe'),
    #         os.path.join(curdir, filename + '.in'),
    #         os.path.join(curdir, filename + '.out')
    #     )