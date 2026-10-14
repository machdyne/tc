# A store to a device register (The Computer).
        lui  x7, 0xE0000     # x7 = 0xE000_0000, the pins' address
        sw   x6, 0(x7)       # send x6 to the pins
