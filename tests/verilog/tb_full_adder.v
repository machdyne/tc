// Testbench for full_adder.v: every input combination, checked
// against ordinary addition.
`timescale 1ns / 1ps

module tb_full_adder;
    reg a, b, cin;
    wire sum, cout;
    integer i, errors;

    full_adder dut (.a(a), .b(b), .cin(cin), .sum(sum), .cout(cout));

    initial begin
        errors = 0;
        for (i = 0; i < 8; i = i + 1) begin
            {a, b, cin} = i;
            #1;
            if ({cout, sum} !== a + b + cin)
                errors = errors + 1;
        end
        if (errors == 0)
            $display("PASS");
        else
            $display("FAIL: %0d errors", errors);
        $finish;
    end
endmodule
