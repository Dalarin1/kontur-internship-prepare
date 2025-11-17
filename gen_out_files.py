import os
import subprocess
import argparse
from tqdm import tqdm


def parse_test_file(input_file_path):
    """
    Парсит .in файл с тестами.
    Возвращает словарь {ID_теста: входные_данные}
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


def run_tests_on_exe(exe_path, input_file_path, output_file_path):
    """
    Запускает тесты на исполняемом файле и генерирует .out файл
    """
    tests = parse_test_file(input_file_path)
    results = {}

    print(f"Запуск тестов из {input_file_path} на {exe_path}")

    for test_id, test_data in tqdm(tests.items()):

        try:
            process = subprocess.Popen(
                [exe_path],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )

            stdout, stderr = process.communicate(input=test_data, timeout=1)

            if process.returncode != 0:
                tqdm.write(
                    f"\033[31m ERROR at:\033[0m {test_id}"
                    f" - returned code {process.returncode}"
                )
                if stderr:
                    tqdm.write(f"\t\033[31m STDERR: \033[0m {stderr}")
                results[test_id] = f"ERROR: return code {process.returncode}"
            else:
                results[test_id] = stdout.strip()

        except subprocess.TimeoutExpired:
            tqdm.write(f"\033[31m Timeout at test\033[0m {test_id}")
            results[test_id] = "ERROR: timeout"
        except Exception as e:
            tqdm.write(
                f"\033[31m Exception at test\033[0m {test_id}: " f" \033[33m{e}\033[0m"
            )
            results[test_id] = f"ERROR: {str(e)}"

    # Записываем результаты в .out файл
    with open(output_file_path, "w", encoding="utf-8") as f:
        for test_id, result in results.items():
            f.write(f"@{test_id}\n")
            f.write(f"{result}\n")

    print(f"Результаты записаны в {output_file_path}")
    return results


def main():
    parser = argparse.ArgumentParser(
        prog="gen_out_files.py",
        epilog="\033[31mWhat have I done...\033[0m",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "season", nargs="?", help="Сезон соревнования (summer-2022, winter-2024...)"
    )
    parser.add_argument(
        "literal", nargs="?", help=".in файлы ('a' или 'abc' для нескольких)"
    )
    parser.add_argument("-e", "--exe", help="Путь к .exe файлу")
    parser.add_argument("-i", "--in", dest="in_file", help="Путь к .in файлу")
    parser.add_argument("-o", "--out", help="Путь к .out файлу")
    args = parser.parse_args()
    season = args.season
    literal = args.literal

    if season is None or literal is None:
        if args.exe is None or args.in_file is None:
            parser.error("Укажите season и literal или все флаги -e, -i, -o")
            return 1
        run_tests_on_exe(args.exe, args.in_file, args.out)

    elif len(literal) > 1:
        for file in literal:
            exe_path = os.path.join(os.curdir, "solution", season, f"{file}.exe")
            in_path = os.path.join(os.curdir, "test", season, f"{file}.in")
            out_path = os.path.join(os.curdir, "test", season, f"{file}.out")

            run_tests_on_exe(exe_path, in_path, out_path)

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

        run_tests_on_exe(exe_path, in_path, out_path)


if __name__ == "__main__":
    main()
