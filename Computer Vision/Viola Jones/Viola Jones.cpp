#include <iostream>
#include <vector>
using namespace std;


void print_vect(vector<std::vector<int>> vec) {
    for (int i = 0; i < vec.size(); i++)
    {
        for (int j = 0; j < vec[i].size(); j++)
        {
            cout << vec[i][j] << ' ';
        }
    cout << std::endl;
    }
    cout << std::endl;
}

vector<std::vector<int>> matrix_res(vector<std::vector<int>> a){
    vector<std::vector<int>> b(a.size(),std::vector<int>(a[0].size()));
    for (int r=0; r<a.size(); r++){
        for (int c=0; c<a[0].size(); c++){
            b[r][c] = a[r][c];
            if (r-1 >= 0 && c-1 >= 0){
                b[r][c] = b[r][c] - b[r-1][c-1];
            }
            if (r-1 >= 0){
                b[r][c] = b[r][c] + b[r-1][c];
            }
            if (c-1 >= 0){
                b[r][c] = b[r][c] + b[r][c-1];
            }
        }
    }
    return b;
}

int main()
{
    vector<std::vector<int>> a {{ 1, 2, 3},
                                        { 4, 5, 6},
                                        { 7, 8, 9} };
    print_vect(a);
    vector<std::vector<int>> c = matrix_res(a);
    print_vect(c);
}
