#include <iostream>
#include <vector>

template <typename T>
inline T min(T a, T b)
{
    if (a <= b)
    {
        return a;
    }
    return b;
}
template <typename T>
inline T max(T a, T b)
{
    if (a > b)
    {
        return a;
    }
    return b;
}

int main()
{
    int height, width, shot_count;
    std::cin >> height >> width >> shot_count;
    // храним карту булов, где 1 - корабль, 0 - не корабль, 2 - подбитый кусок корабля
    std::vector<std::vector<char>> map;
    char temp;

    for (int i = 0; i < height; i++)
    {
        map.push_back(std::vector<char>());
        for (int j = 0; j < width; j++)
        {
            std::cin >> temp;

            // По условию X обозначает часть корабля в данной точке
            map[i].push_back(static_cast<char>(temp == 'X'));
        }
    }
    int i, j;
    bool has_neighbour = false;
    while (shot_count--)
    {
        has_neighbour = false;
        std::cin >> i >> j;
        i--;
        j--;
        if (map[i][j] == 0)
        {
            std::cout << "MISS" << std::endl;
            continue;
        }
        if (i > 0 && map[i-1][j] > 0){has_neighbour = true;}
        else if(i < height - 1 && map[i+1][j] > 0){has_neighbour = true;}
        else if(j > 0 && map[i][j-1] > 0){has_neighbour = true;}
        else if(j < width - 1 && map[i][j+1] > 0){has_neighbour=true;}
        
        if (map[i][j] == 1 && has_neighbour)
        {
            std::cout << "HIT" << std::endl;
            map[i][j] = false;
            continue;
        }
        std::cout << "DESTROY" << std::endl;
        map[i][j] = false;
    }
    return 0;
}