import os
import subprocess
import sys
from tqdm import tqdm
import argparse


def parse_out_file(out_file_path):
    """
    Парсит .out файл <br>
    Возвращает словарь {ID_теста : ожидаемый_вывод}
    """
    expected_results = {}

    with open(out_file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Разделяем на тесты по @test-
    test_blocks = content.split("@")

    for block in test_blocks:
        if not block.strip() or not block.startswith("test-"):
            continue

        # Извлекаем ID теста и ожидаемый результат
        lines = block.strip().split("\n")
        test_id = lines[0].strip()
        expected_result = "\n".join(lines[1:]).strip()

        expected_results[test_id] = expected_result

    return expected_results


def check_solution(exe_path, in_file, expected_out_file, detailed_err=False):
    """
    Проверяет решение на тестах
    """
    # Получаем тесты из .in файла
    tests = parse_test_file(in_file)

    # Получаем ожидаемые результаты из .out файла
    expected_results = parse_out_file(expected_out_file)

    passed_tests = 0
    failed_tests = 0

    print(f"Checking \t {exe_path}")
    print(f"Input file \t {in_file}")
    print(f"Output file: \t {expected_out_file}")

    for test_id, test_data in tqdm(tests.items()):

        if test_id not in expected_results:
            tqdm.write(
                f"\r\033[35m Warning: {test_id} not found in {expected_out_file}\033[0m"
            )
            continue

        expected = expected_results[test_id]

        try:

            process = subprocess.Popen(
                [exe_path],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )

            stdout, stderr = process.communicate(input=test_data, timeout=1)
            actual = stdout.strip()

            if process.returncode != 0:
                tqdm.write(
                    f"\033[31m ERROR at:\033[0m {test_id} - returned code {process.returncode}"
                )
                if stderr:
                    tqdm.write(f"\t\033[31m STDERR: \033[0m {stderr}")
                failed_tests += 1
            elif actual == expected:
                passed_tests += 1
            else:
                tqdm.write(f"\033[31m Wrong anser at test\033[0m {test_id}")
                failed_tests += 1

        except subprocess.TimeoutExpired:
            tqdm.write(f"\033[31m Timeout at test\033[0m {test_id}")
            failed_tests += 1
        except Exception as e:
            tqdm.write(
                f"\033[31m Exception at test\033[0m {test_id}: \033[33m{e}\033[0m"
            )
            failed_tests += 1

    print(
        f"\033[32m Passed \033[0m: {passed_tests},\033[31m Failed \033[0m: {failed_tests}"
    )
    print()

    # TODO
    # после завершения выводим различия в выходных данных
    if detailed_err:
        pass
    return passed_tests, failed_tests


def parse_test_file(input_file_path):
    """
    Парсит .in файл <br>
    Возвращает словарь {ID_теста : входные_данные}
    """
    tests = {}

    with open(input_file_path, "r", encoding="utf-8") as f:
        content = f.read()

    test_blocks = content.split("@")

    for block in test_blocks:
        if not block.strip() or not block.startswith("test-"):
            continue

        lines = block.strip().split("\n")
        test_id = lines[0].strip()
        test_data = "\n".join(lines[1:]).strip()

        tests[test_id] = test_data

    return tests


def main():
    """
    :args: python check.py <season> <literal> [-e [direct-path-to-exe]] [-i [direct-path-to-in-file]] [-o [direct-path-to-out-file]]
    :season: any of summer-2022 / summer-2023 / summer-2025 / winter-2024
    :literal: r"[abcde]+"
    """

    parser = argparse.ArgumentParser(
        prog="check.py",
        description="""
        Validate solution on .in / .out test files
        Usage: 
            check.py winter-2024 a -> validates a.exe on test/winter-2024/a
            
            check.py winter-2024 abc -> validates a.exe on test/winter-2024/a
                                     -> validates b.exe on test/winter-2024/b
                                     -> validates c.exe on test/winter-2024/c
            
            check.py -e ./solution/exe -i test.in -o test.out""",
        epilog="\033[31m What have I done...\033[0m",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        "season",
        nargs="?",
        help="Contest season identifier (summer-2022, winter-2024 etc). "
        "Required unless using direct file paths with -e/-i/-o flags.",
    )
    parser.add_argument(
        "literal",
        nargs="?",
        help="Solution files ('a' for a.exe, 'abc' for a.exe, b.exe, c.exe). "
        "Required unless using direct file paths with -e/-i/-o flags.",
    )
    parser.add_argument("-e", "--exe", help="Specified path to .exe file")
    parser.add_argument("-i", "--in", dest="in_file", help="Specified path to .in file")
    parser.add_argument("-o", "--out", help="Specified path to .out file")

    args = parser.parse_args()
    season = args.season
    literal = args.literal

    if season is None or literal is None:
        if args.exe is None or args.in_file is None or args.out is None:
            parser.error(
                "Either specify season and literal or provide -e, -i and -o flags"
            )
            sys.exit(1)

        check_solution(args.exe, args.in_file, args.out)

    elif len(literal) > 1:
        for file in literal:

            exe_path = os.path.join(os.curdir, "solution", season, f"{file}.exe")
            in_path = os.path.join(os.curdir, "test", season, f"{file}.in")
            out_path = os.path.join(os.curdir, "test", season, f"{file}.out")

            check_solution(exe_path, in_path, out_path)

    else:
        exe_path = (
            args.exe
            if args.exe
            else os.path.join(os.curdir, "solution", season, f"{literal}.exe")
        )
        in_path = (
            args.in_file
            if args.in_file
            else os.path.join(os.curdir, "test", season, f"{literal}.in")
        )
        out_path = (
            args.out
            if args.out
            else os.path.join(os.curdir, "test", season, f"{literal}.out")
        )

        check_solution(exe_path, in_path, out_path)


if __name__ == "__main__":
    main()
