#include <stdio.h>

#define BIT(n) (1u << (n))

int main(void)
{
    unsigned flags = 0;

    flags |= BIT(3);            /* set bit 3 */
    flags |= BIT(0);            /* set bit 0 */
    flags &= ~BIT(3);           /* clear bit 3 */
    flags ^= BIT(5);            /* flip bit 5 */

    if (flags & BIT(0))         /* test bit 0 */
        printf("bit 0 is set\n");

    printf("flags = 0x%02X\n", flags);
    return 0;
}
