module top(
    input d,
    input clk,
    input pre,
    output reg q
);
    initial q = 1'b0;
    always @(posedge clk, posedge pre) begin
       if (pre)
          q <= 1'b1;
       else
          q <= d;
    end
endmodule
