#include <iostream>
#include <vector>
#include <algorithm>

int left_bound(const std::vector<int> &arr, int value)
{
    int left = 0;
    int right = arr.size() - 1;
    int result = -1;
    while (left <= right)
    {
        int mid = left + (right - left) / 2;
        if (arr[mid] <= value)
        {
            result = mid;
            left = mid + 1;
        }
        else
        {
            right = mid - 1;
        }
    }
    return result;
}

int main()
{
    int N; // x - граница
    int M; // y - граница
    int U; // количество прямых в OY
    int V; // количество прямых в OX

    std::cin >> N >> M;
    std::cin >> U >> V;

    std::vector<int> verticals;
    verticals.resize(U + 2);
    verticals[0] = 0;
    for (int i = 1; i < U + 1; i++)
    {
        std::cin >> verticals[i];
    }
    verticals[verticals.size() - 1] = N;
    std::sort(verticals.begin(), verticals.end());

    std::vector<int> horisontals;
    horisontals.resize(V + 2);
    horisontals[0] = 0;
    for (int i = 1; i < V + 1; i++)
    {
        std::cin >> horisontals[i];
    }
    horisontals[horisontals.size() - 1] = M;
    std::sort(horisontals.begin(), horisontals.end());

    int call_count;
    std::cin >> call_count;
    int x1, y1, x2, y2;

    while (call_count > 0)
    {
        call_count--;
        std::cin >> x1 >> y1 >> x2 >> y2;

        if (left_bound(horisontals, y1) != left_bound(horisontals, y2) ||
            left_bound(verticals, x1) != left_bound(verticals, x2))
        {
            std::cout << "NO" << std::endl;
        }
        else
        {
            std::cout << "YES" << std::endl;
        }
    }
    return 0;
}