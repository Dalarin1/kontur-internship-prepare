import sys
import os

TEST_DIR = os.getcwd() + "/test"
years_folders = [i for i in os.listdir(TEST_DIR) if i != "include"]
years_folders.remove("summer-2022")

for year in years_folders:
    fullpath = TEST_DIR + "/" + year

    for file in os.listdir(fullpath):
        print(fullpath + "/" + file)

        cmd = f"g++ -o {fullpath + '/' + file.replace('.cpp', '.exe')} -I {TEST_DIR}/include -O3 -s {fullpath + '/' + file}"
        if os.system(cmd) == 0:
            print(f"✓ Успешно: {file}")
        else:
            print(f"✗ Ошибка: {file}")

        # os.execlp(
        #     "g++",
        #     "g++",  # argv[0]
        #     "-o",
        #     f"{fullpath + '/' + file.replace('.cpp', '.exe')}",  # отдельные аргументы
        #     "-I",
        #     "../include",
        #     "-O3",
        #     "-s",
        #     fullpath + '/' + file,
        # )
