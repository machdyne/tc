// A peripheral with one register: a byte the CPU can write and read
// back, whose bits drive eight LEDs.
module led_reg (
    input  wire        clk,
    input  wire        reset,
    input  wire        sel,        // the bus is addressing this device
    input  wire        we,         // and it is a write
    input  wire [31:0] wdata,      // the data the CPU is writing
    output wire [31:0] rdata,      // the data the CPU reads
    output wire [7:0]  leds
);
    reg [7:0] value;

    always @(posedge clk)
        if (reset)
            value <= 8'd0;
        else if (sel && we)
            value <= wdata[7:0];

    assign rdata = {24'd0, value};
    assign leds  = value;
endmodule
