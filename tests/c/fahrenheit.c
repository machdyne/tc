#include <stdio.h>

int main(void)
{
    for (int c = 0; c <= 100; c += 20)
        printf("%d %d\n", c, c * 9 / 5 + 32);
    return 0;
}
