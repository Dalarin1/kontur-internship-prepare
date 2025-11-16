#include <iostream>
#include <vector>
#include <queue>
#include <set>

bool is_ship_alive(const std::vector<std::vector<char>> &map, int i, int j)
{
    int height = map.size();
    int width = map[0].size();
    bool result = false;
    auto ship = std::queue<std::pair<int, int>>();
    auto visited = std::set<std::pair<int, int>>();
    ship.emplace(std::pair<int, int>(i, j));

    std::pair<int, int> temp;

#define y temp.first
#define x temp.second

    while (!ship.empty())
    {
        temp = ship.front();
        visited.insert(temp);
        ship.pop();
        if (map[y][x] == 'X')
        {
            return true;
        }
        if (map[y][x] == '~')
        {
            // Осмотр и добавление еще не посещенных соседей соседей, которые не '.'
            if (y > 0 && map[y - 1][x] != '.' && visited.find(std::pair(y - 1, x)) == visited.end())
            {
                ship.push(std::pair(y - 1, x));
            }
            if (y < height - 1 && map[y + 1][x] != '.' && visited.find(std::pair(y + 1, x)) == visited.end())
            {
                ship.push(std::pair(y + 1, x));
            }
            if (x > 0 && map[y][x - 1] != '.' && visited.find(std::pair(y, x - 1)) == visited.end())
            {
                ship.push(std::pair(y, x - 1));
            }
            if (x < width - 1 && map[y][x + 1] != '.' && visited.find(std::pair(y, x + 1)) == visited.end())
            {
                ship.push(std::pair(y, x + 1));
            }
        }
    }
#undef x
#undef y
    return false;
}

int main()
{
    int height, width, shot_count;
    std::cin >> height >> width >> shot_count;
    // храним карту чаров, где X - корабль, . - не корабль, ~ - подбитый кусок корабля
    std::vector<std::vector<char>> map;
    char temp;

    for (int i = 0; i < height; i++)
    {
        map.push_back(std::vector<char>());
        for (int j = 0; j < width; j++)
        {
            std::cin >> temp;
            map[i].push_back(temp);
        }
    }
    int i, j;

    while (shot_count--)
    {

        std::cin >> i >> j;
        // входные координаты начинаются с 1, 1
        i--;
        j--;
        if (map[i][j] == '.')
        {
            std::cout << "MISS" << std::endl;
            continue;
        }

        
        map[i][j] = '~';
        if (is_ship_alive(map, i, j))
        {
            std::cout << "HIT" << std::endl;
        }
        else
        {
            std::cout << "DESTROY" << std::endl;
        }
    }
    return 0;
}