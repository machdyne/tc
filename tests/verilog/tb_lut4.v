// Testbench for lut4.v: the same block configured as two different
// functions of its inputs.
`timescale 1ns / 1ps

module tb_lut4;
    reg [3:0] in;
    wire xor01, and4;
    integer i, errors;

    lut4 #(.INIT(16'h6666)) as_xor (.in(in), .out(xor01));  // in[0] ^ in[1]
    lut4 #(.INIT(16'h8000)) as_and (.in(in), .out(and4));   // all four

    initial begin
        errors = 0;
        for (i = 0; i < 16; i = i + 1) begin
            in = i;
            #1;
            if (xor01 !== (in[0] ^ in[1])) errors = errors + 1;
            if (and4 !== (&in)) errors = errors + 1;
        end
        if (errors == 0)
            $display("PASS");
        else
            $display("FAIL: %0d errors", errors);
        $finish;
    end
endmodule
