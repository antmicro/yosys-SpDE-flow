module top( x, y, A );
    input [1:0] x;
    input [1:0] y;
    output [3:0] A;
    assign A =  x * y;
endmodule
