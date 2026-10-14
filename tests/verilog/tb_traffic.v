// Testbench for traffic.v: reset to red, then step through the cycle,
// and check that nothing moves while the timer is still running.
`timescale 1ns / 1ps

module tb_traffic;
    reg clk = 0, reset = 1, done = 0;
    wire green, yellow, red;
    integer errors = 0;

    traffic dut (.clk(clk), .reset(reset), .done(done),
                 .green(green), .yellow(yellow), .red(red));

    always #5 clk = ~clk;

    task expect_lights(input g, input y, input r);
        begin
            if ({green, yellow, red} !== {g, y, r}) begin
                errors = errors + 1;
                $display("lights %b%b%b, wanted %b%b%b",
                         green, yellow, red, g, y, r);
            end
        end
    endtask

    task step(input d);
        begin
            done = d;
            @(posedge clk);
            #1;
        end
    endtask

    initial begin
        step(0);
        reset = 0;
        expect_lights(0, 0, 1);
        step(0); expect_lights(0, 0, 1);   // timer running: stay
        step(1); expect_lights(1, 0, 0);
        step(1); expect_lights(0, 1, 0);
        step(0); expect_lights(0, 1, 0);
        step(1); expect_lights(0, 0, 1);
        step(1); expect_lights(1, 0, 0);
        if (errors == 0)
            $display("PASS");
        else
            $display("FAIL: %0d errors", errors);
        $finish;
    end
endmodule
