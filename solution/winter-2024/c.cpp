#include <iostream>
#include <vector>
#include <algorithm>

int main()
{
    int N; // количество зданий
    int k; // максимальная высота здания
    int q; // скольким зданиям можно сделать высоту 1

    std::cin >> N >> k >> q;
    std::vector<int> buildings;
    buildings.reserve(N);
    for (int i = 0; i < N; i++)
    {
        std::cin >> buildings[i];
    }
    // решаем двумя указателями
    int left = 0;
    int right = 0;
    int maxLen = 0;
    int counter = 0;

    while (right < N)
    {
        if (buildings[right] < k)
        {
            right++;
            continue;
        }
        if (counter < q){
            right++;
            counter++;
            continue;
        }

        maxLen = std::max(maxLen, right - left);

        while(buildings[left] < k){
            left++;
        }

        right++;
        left++;
    }
    maxLen = std::max(maxLen, right - left);
    std::cout<<maxLen;
    return 0;
}