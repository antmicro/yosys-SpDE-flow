module top(input en, input dat, output reg q);
    always @* begin
        if (en)
           q <= dat;
    end
endmodule
