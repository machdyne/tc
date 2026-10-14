// A model of a 4-input look-up table: sixteen stored bits, and the
// four inputs choose which one appears at the output. Not a listing in
// the book: it checks the INIT values quoted in Inside an FPGA.
module lut4 #(
    parameter [15:0] INIT = 16'h0000
) (
    input  wire [3:0] in,
    output wire       out
);
    assign out = INIT[in];
endmodule
