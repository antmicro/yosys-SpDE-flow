module top ( led, clk );
    output [1:0] led;
    input clk;
    reg [31:0] counter;

    always @(posedge clk)
       counter <= counter + 1;

    assign led[1:0] = counter[31:30];
endmodule
