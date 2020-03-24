module top (oe, inp, outp, bidir);

// Port Declaration

input   oe;
input   inp;
output  outp;
inout   bidir;

reg     a;
reg     b;

assign bidir = oe ? a : 8'bZ ;
assign outp  = b;

// Always Construct

always @*
begin
    b <= bidir;
    a <= inp;
end

endmodule
