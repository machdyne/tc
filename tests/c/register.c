/* Talking to hardware through a memory-mapped register. Compiled only:
   the address is a device on the target machine, not on the host. */

#include <stdint.h>

#define PINS (*(volatile uint32_t *)0xE0000000u)

void led_on(void)  { PINS |= 1u; }
void led_off(void) { PINS &= ~1u; }

int main(void)
{
    led_on();
    led_off();
    return 0;
}
