import os
import random
import string
from math import comb


def random_sequencce(start, end, num_points=None):
    """Генерирует случайную возрастающую последовательность в интервале [start, end]."""
    interval_length = abs(end - start)

    if num_points is None:
        num_points = random.randint(1, interval_length)

    if num_points <= 0:
        return []

    sequence = []
    current = start

    step = max(1, interval_length // num_points)

    for _ in range(num_points):
        current = random.randint(current, min(current + step, end))
        sequence.append(current)
        if current >= end:
            break

    return sequence


def randgraph(rooms_count, coridors_count):
    rooms = [i for i in range(1, rooms_count + 1)]
    coridors: set[tuple] = set()

    for _ in range(coridors_count):
        r_from, r_to = random.choice(rooms), random.choice(rooms)
        while (r_from, r_to) in coridors or r_from == r_to:
            r_from, r_to = random.choice(rooms), random.choice(rooms)
        coridors.add((r_from, r_to))

    coridors = [list(pair) for pair in coridors]
    for i in range(len(coridors)):
        coridors[i] += [random.randint(0, 10)]
    return coridors


# winter-2024
TEST_DIR = os.path.join(os.getcwd(), "test")
curdir = os.path.join(TEST_DIR, "winter-2024")


class Winter2024:

    @staticmethod
    def gen_A():
        file_in = os.path.join(curdir, "a.in")
        basetest = ["@test-1\n5\neeeeee\njjjjjjjj\neww\nabc\nrty\n"]

        with open(file_in, "w", encoding="utf-8") as f:
            f.writelines(basetest)
            test_id = ""
            for iter in range(len(basetest) + 1, 30):
                test_id = f"@test-{iter}\n"
                testnum = random.randint(1, 10)
                testcases = [
                    "".join(
                        [
                            random.choice(string.ascii_lowercase)
                            for _ in range(random.randint(3, 30))
                        ]
                    )
                    + "\n"
                    for _ in range(testnum)
                ]
                f.write(test_id)
                f.write(str(testnum) + "\n")
                f.write("".join(testcases))

    @staticmethod
    def gen_B():
        file_in = os.path.join(curdir, "b.in")
        basetests = [
            "4\n1 1\n10 10\n16 0\n0 16\n8 17\n-2 23\n14 7\n-1 8\n",
            "2\n0 0\n7 7\n5 14\n-2 7\n",
        ]
        with open(file_in, "w", encoding="utf-8") as f:
            f.writelines(basetests)
            test_id = ""

            for iter in range(len(basetests) + 1, 30):
                test_id = f"@test-{iter}\n"
                testnum = random.randint(1, 10)
                points = (
                    "\n".join(
                        [
                            str(random.randint(-100, 100))
                            + " "
                            + str(random.randint(-100, 100))
                            for _ in range(testnum)
                        ]
                    )
                    + "\n"
                )

                f.write(test_id)
                f.write(str(testnum))
                f.write(points)

    @staticmethod
    def gen_C():
        file_in = os.path.join(curdir, "c.in")

        # Базовые тесты из условия
        basetests = ["@test-1\n5 6 1\n7 2 7 4 7\n", "@test-2\n6 7 1\n100 7 6 3 4 5\n"]

        with open(file_in, "w", encoding="utf-8") as f:
            f.writelines(basetests)

            for iter in range(len(basetests) + 1, 30):
                test_id = f"@test-{iter}\n"

                # Генерируем параметры
                n = random.randint(1, 100000)
                k = random.randint(2, 1000000)
                q = random.randint(0, 100000)

                # Генерируем высоты зданий
                heights = [str(random.randint(1, 1000000)) for _ in range(n)]

                f.write(test_id)
                f.write(f"{n} {k} {q}\n")
                f.write(" ".join(heights) + "\n")

    @staticmethod
    def gen_D():
        file_in = os.path.join(curdir, "d.in")

        # Базовые тесты из условия
        basetests = [
            "@test-1\n10 7\n4 3\n1 9 6 4\n5 2 6\n3\n2 1 3 1\n5 1 5 3\n7 3 8 4\n",
            "@test-2\n10 6\n3 1\n9 6 4\n2\n2\n2 3 3 5\n5 3 7 1\n",
        ]

        with open(file_in, "w", encoding="utf-8") as f:
            f.writelines(basetests)

            for iter in range(len(basetests) + 1, 30):
                test_id = f"@test-{iter}\n"

                # Генерируем размеры карты
                N = random.randint(5, 1000)
                M = random.randint(5, 1000)

                # Генерируем количество прямых
                U = random.randint(1, min(100, N - 1))
                V = random.randint(1, min(100, M - 1))

                # Генерируем прямые (уникальные)
                ui = sorted(random.sample(range(1, N), U))
                vj = sorted(random.sample(range(1, M), V))

                # Генерируем запросы
                q = random.randint(1, 100)

                f.write(test_id)
                f.write(f"{N} {M}\n")
                f.write(f"{U} {V}\n")
                f.write(" ".join(map(str, ui)) + "\n")
                f.write(" ".join(map(str, vj)) + "\n")
                f.write(f"{q}\n")

                # Генерируем точки запросов (гарантируем, что не на прямых)
                for _ in range(q):
                    while True:
                        x1 = random.randint(1, N)
                        if all(x1 != u for u in ui):
                            break
                    while True:
                        y1 = random.randint(1, M)
                        if all(y1 != v for v in vj):
                            break
                    while True:
                        x2 = random.randint(1, N)
                        if all(x2 != u for u in ui):
                            break
                    while True:
                        y2 = random.randint(1, M)
                        if all(y2 != v for v in vj):
                            break

                    f.write(f"{x1} {y1} {x2} {y2}\n")

    @staticmethod
    def gen_E():

        from collections import deque

        file_in = os.path.join(curdir, "e.in")

        def generate_ship(grid, n, m, min_size=1, max_size=10):
            """Генерирует один корабль на сетке"""
            attempts = 0
            while attempts < 100:
                i = random.randint(0, n - 1)
                j = random.randint(0, m - 1)
                if grid[i][j] == ".":
                    break
                attempts += 1
            else:
                return False

            ship_cells = []
            size = random.randint(min_size, max_size)

            queue = deque([(i, j)])
            visited = set([(i, j)])

            while queue and len(ship_cells) < size:
                ci, cj = queue.popleft()
                ship_cells.append((ci, cj))
                grid[ci][cj] = "X"

                directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
                random.shuffle(directions)

                for di, dj in directions:
                    ni, nj = ci + di, cj + dj
                    if (
                        0 <= ni < n
                        and 0 <= nj < m
                        and grid[ni][nj] == "."
                        and (ni, nj) not in visited
                        and len(ship_cells) < size
                    ):

                        valid = True
                        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                            nx, ny = ni + dx, nj + dy
                            if (
                                0 <= nx < n
                                and 0 <= ny < m
                                and grid[nx][ny] == "X"
                                and (nx, ny) not in ship_cells
                            ):
                                valid = False
                                break

                        if valid:
                            visited.add((ni, nj))
                            queue.append((ni, nj))

            return True

        # Базовые тесты из условия
        basetests = [
            "@test-1\n4 4 6\n.XXX\n....\nX.X.\n...X\n1 3\n1 2\n1 4\n3 1\n3 3\n4 4\n",
            "@test-2\n4 3 7\nXX.\n.XX\n..X\nX..\n2 2\n3 3\n2 1\n1 2\n1 1\n2 3\n4 1\n",
        ]

        with open(file_in, "w", encoding="utf-8") as f:
            f.writelines(basetests)

            for iter in range(len(basetests) + 1, 30):
                test_id = f"@test-{iter}\n"

                # Генерируем размеры поля
                n = random.randint(4, 20)
                m = random.randint(4, 20)
                q = random.randint(1, min(50, n * m))

                # Создаем пустую сетку
                grid = [["." for _ in range(m)] for _ in range(n)]

                # Генерируем корабли
                num_ships = random.randint(2, 8)
                for _ in range(num_ships):
                    generate_ship(grid, n, m, 1, 5)

                # Генерируем выстрелы (уникальные)
                shots = set()
                while len(shots) < q:
                    i = random.randint(1, n)
                    j = random.randint(1, m)
                    shots.add((i, j))

                f.write(test_id)
                f.write(f"{n} {m} {q}\n")

                # Записываем сетку
                for row in grid:
                    f.write("".join(row) + "\n")

                # Записываем выстрелы
                for i, j in shots:
                    f.write(f"{i} {j}\n")

    @staticmethod
    def generate():
        Winter2024.gen_A()
        Winter2024.gen_B()
        Winter2024.gen_C()
        Winter2024.gen_D()
        Winter2024.gen_E()


curdir = os.path.join(TEST_DIR, "summer-2025")


class Summer2025:
    @staticmethod
    def gen_A():

        cards_values = "23456789TJQKA"
        cards_faces = "CDHS"

        test_count = 30
        file_in = os.path.join(curdir, "a.in")

        with open(file_in, "w", encoding="utf-8") as f:
            basetest = "2 1 3 1\n9H\nQH\nK\n2H\n3D\n4C\n5CDH\n"
            f.write("@test-1\n")
            f.write(basetest)

            for i in range(1, test_count):
                r1, s1, r2, s2 = [
                    random.randint(1, 5) for _ in range(4)
                ]  # 1 <= r1 + s1 + r2 + s2 <= 100
                testcase = ""
                for _ in range(r1 + s1 + r2 + s2):
                    rnd_subsequence = list(
                        set(
                            random.choices(cards_values, k=random.randint(0, 13))
                            + random.choices(cards_faces, k=random.randint(0, 4))
                        )
                    )
                    rnd_subsequence.sort()
                    # Собрать N случайных из cards_values и M случайных из мастей (все уникальны)

                    # Гарантия наличия чего-нибудь в rnd_subsequence
                    if not rnd_subsequence:
                        if random.randint(0, 1):
                            rnd_subsequence = random.choice(cards_values)
                        else:
                            rnd_subsequence = random.choice(cards_faces)
                    testcase += "".join(rnd_subsequence) + "\n"
                test_id = f"@test-{i+1}\n"
                f.write(test_id)
                f.write(f"{r1} {s1} {r2} {s2}\n")
                f.write(testcase)

    @staticmethod
    def gen_B():
        file_in = os.path.join(curdir, "b.in")
        test_count = 30
        basetests = ["3 1\n1 3 5\n3\n", "4 2\n1 2 3 4\n1 4\n"]

        with open(file_in, "w", encoding="utf-8") as f:
            for i, test in enumerate(basetests):
                f.write(f"@test-{i}\n")
                f.write(test)
            for i in range(1, test_count):
                N = random.randint(1, 10)
                M = random.randint(1, 10)
                ns = " ".join(str(i) for i in random_sequencce(1, 30, N)) + "\n"
                ms = " ".join(str(i) for i in random_sequencce(1, 30, M)) + "\n"

                f.write(f"@test-{i+1}\n")
                f.write(f"{N} {M}\n")
                f.write(ns)
                f.write(ms)

    @staticmethod
    def gen_C():
        file_in = os.path.join(curdir, "c.in")
        test_count = 30
        basetests = [
            "11 20\n7 7 5 20 8 8 8 20 20 5 5\n",
            "12 20\n7 7 5 20 8 7 8 8 20 20 5 5\n",
        ]

        with open(file_in, "w", encoding="utf-8") as f:
            for i, test in enumerate(basetests):
                f.write(f"@test-{i}\n")
                f.write(test)
            for i in range(1, test_count):
                N, M = [random.randint(1, 10), random.randint(1, 10)]
                ns = " ".join([str(random.randint(1, M)) for _ in range(N)]) + "\n"

                f.write(f"@test-{i+1}\n")
                f.write(f"{N} {M}\n")
                f.write(ns)

    @staticmethod
    def gen_D():

        file_in = os.path.join(curdir, "d.in")
        test_count = 30
        basetests = [
            "6 6 4\n1 2 1\n2 4 3\n4 5 6\n5 6 5\n4 3 2\n3 2 7\n",
            "6 6 4\n1 2 4\n2 4 3\n4 5 6\n5 6 5\n4 3 2\n3 2 3\n",
            "2 1 2\n1 2 0\n",
        ]

        with open(file_in, "w", encoding="utf-8") as f:
            for i, test in enumerate(basetests):
                f.write(f"@test-{i}\n")
                f.write(test)
            for i in range(2, test_count):

                a = random.randint(2, 10)
                b = random.randint(1, comb(2, a))
                c = random.randint(0, 30)

                graph = "\n".join(
                    " ".join(str(j) for j in i)
                    for i in randgraph(rooms_count=a, coridors_count=b)
                )

                test_id = f"@test-{i+1}\n"
                f.write(test_id)
                f.write(f"{a} {b} {c}\n")
                f.write(f"{graph}\n")

    # TODO
    @staticmethod
    def gen_E():
        file_in = os.path.join(curdir, "e.in")
        test_count = 30
        basetests = [
            "2 4 11\n3 3\n+ 1 3 another\n+ 1 2 secret\n+ 1 2 secret\nc 1 2 sec\np 2 2 new\n+ 2 4 string\nc 2 2 news\n+ 2 4 strong\nc 1 2 news\nc 1 4 str\nc 1 5 ano\n",
            "3 8 11\n3 4 5\n+ 3 4 abcd\n+ 3 2 abcd\n+ 3 4 abee\n+ 3 2 abea\np 3 4 qq\np 3 2 qqe\nc 3 4 qqabc\nc 3 2 qqeab\nc 1 2 qqeabe\n+ 1 4 qqab\nc 1 4 qqab\n",
            "2 2 5\n4 1\n+ 2 1 abc\n+ 2 1 abe\np 1 3 pr\nc 1 3 pr\nc 2 1 prabc\n",
        ]
        with open(file_in, "w", encoding="utf-8") as f:
            for i, test in enumerate(basetests):
                f.write(f"@test-{i}\n")
                f.write(test)
            for i in range(2, test_count):
                N, K, Q = (random.randint(1, 10) for _ in range(3))
                ms = [random.randint(1, 10) for _ in range(N)]

                pass


if __name__ == "__main__":

    Summer2025.gen_E()
