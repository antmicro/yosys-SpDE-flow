module simple_arr(
   input [1:0] in,
   output z
);
    assign z = in[1] | in[0];
endmodule
