module simple_comb(
    input a,
    input b,
    input c,
    input d,
    output out
);
    assign out = (a & (~ b)) | (c & d);
endmodule
