// Testbench for blink.v: a 4-bit counter, so the LED must change
// every 8 clock cycles.
`timescale 1ns / 1ps

module tb_blink;
    reg clk = 0;
    wire led;
    integer i, changes;
    reg last;

    blink #(.WIDTH(4)) dut (.clk(clk), .led(led));

    always #5 clk = ~clk;

    initial begin
        changes = 0;
        last = 0;
        for (i = 0; i < 64; i = i + 1) begin
            @(posedge clk);
            #1;
            if (led !== last) begin
                changes = changes + 1;
                last = led;
            end
        end
        // 64 cycles, a change every 8: 8 changes
        if (changes == 8)
            $display("PASS");
        else
            $display("FAIL: %0d changes", changes);
        $finish;
    end
endmodule
