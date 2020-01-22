module top ( led );
    output [2:0] led;
    reg [15:0] counter;

    wire Sys_Clk0;
    // wire Sys_Clk0_Rst;

    // gclkbuff u_gclkbuff_reset ( .A(Sys_Clkdd0_Rst | WB_RST ), .Z(WB_RST_FPGA) );
    gclkbuff u_gclkbuff_clock ( .A(Sys_Clk0), .Z(WB_CLK) );

    qlal4s3b_cell_macro u_qlal4s3b_cell_macro (
        .Sys_Clk0 ( Sys_Clk0 )
    );

    always @(posedge WB_CLK)
          counter <= counter + 1;
    assign led[2:0] = counter[15:13];
endmodule
