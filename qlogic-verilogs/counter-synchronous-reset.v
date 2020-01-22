module top ( out, clk, reset );
    output [3:0] out;
    input clk, reset;
    reg [3:0] out;

    always @(posedge clk)
      if (reset)
          out <= 4'b0;
      else
          out <= out + 1;
endmodule
