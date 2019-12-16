module simple_lut(
   input a, b, c,
   output z
);
    assign z = (~a & ~b & c) | (a & b & ~c);
endmodule
