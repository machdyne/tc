// Testbench for led_reg.v. It plays the part of the bus: an address
// decoder selects the device at 0xE000_0000, and the "CPU" performs
// the same read-modify-write as led_on() in tests/c/register.c.
`timescale 1ns / 1ps

module tb_led_reg;
    reg clk = 0, reset = 1, we = 0;
    reg [31:0] addr = 0, wdata = 0;
    wire [31:0] rdata;
    wire [7:0] leds;
    integer errors = 0;

    // the address decoder: the top four bits pick the device
    wire sel = (addr[31:28] == 4'hE);

    led_reg dut (.clk(clk), .reset(reset), .sel(sel), .we(we),
                 .wdata(wdata), .rdata(rdata), .leds(leds));

    always #5 clk = ~clk;

    task write(input [31:0] a, input [31:0] d);
        begin
            addr = a; wdata = d; we = 1;
            @(posedge clk); #1;
            we = 0;
        end
    endtask

    initial begin
        @(posedge clk); #1;
        reset = 0;
        if (leds !== 8'h00) errors = errors + 1;

        write(32'hE000_0000, 32'h0000_00A0);
        if (leds !== 8'hA0) errors = errors + 1;

        // led_on(): read the register, set bit 0, write it back
        addr = 32'hE000_0000; #1;
        write(32'hE000_0000, rdata | 32'h1);
        if (leds !== 8'hA1) errors = errors + 1;

        // a write to another device's address must not change it
        write(32'h4000_0000, 32'h0000_00FF);
        if (leds !== 8'hA1) errors = errors + 1;

        if (errors == 0)
            $display("PASS");
        else
            $display("FAIL: %0d errors", errors);
        $finish;
    end
endmodule
