module top(
    input d,
    input clk,
    input en,
    output reg q
);
    initial q = 1'b0;
    always @(posedge clk) begin
       if (en)
          q <= d;
    end
endmodule
