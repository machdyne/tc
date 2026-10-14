#include <stdio.h>

int gcd(int a, int b)
{
    while (b != 0) {
        int t = a % b;
        a = b;
        b = t;
    }
    return a;
}

int main(void)
{
    printf("%d\n", gcd(1071, 462));
    return 0;
}
