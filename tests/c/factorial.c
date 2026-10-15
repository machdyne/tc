#include <stdio.h>

int factorial(int n)
{
    int f = 1;
    for (int i = 1; i <= n; i++)
        f *= i;
    return f;
}

int main(void)
{
    printf("%d\n", factorial(7));
    return 0;
}
