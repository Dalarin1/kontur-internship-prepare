#include <iostream>

int main()
{
    int N;
    int temp_x, temp_y;
    float sum_x1, sum_y1;
    float sum_x2, sum_y2;

    std::cin >> N;
    for (int i = 0; i < N; i++)
    {
        std::cin >> temp_x >> temp_y;
        sum_x1 += temp_x;
        sum_y1 += temp_y;
    }
    for (int i = 0; i < N; i++)
    {
        std::cin >> temp_x >> temp_y;
        sum_x2 += temp_x;
        sum_y2 += temp_y;
    }
    std::cout << static_cast<int>(sum_x2 / N - sum_x1 / N) << ' ' << static_cast<int>(sum_y2 / N - sum_y1 / N) << std::endl;
    return 0;
}