#include <stdio.h>

/* Count the characters in a string by walking a pointer along it
   until it reaches the zero byte that ends every C string. */
int length(const char *s)
{
    const char *p = s;
    while (*p != '\0')
        p++;
    return p - s;
}

int main(void)
{
    int x = 42;
    int *p = &x;            /* p holds the address of x */
    *p = 7;                 /* store 7 at that address */
    printf("x is now %d\n", x);

    int a[4] = { 10, 20, 30, 40 };
    int *q = a;             /* the array's first address */
    printf("%d %d\n", *(q + 2), q[3]);

    printf("%d\n", length("timeless"));
    return 0;
}
