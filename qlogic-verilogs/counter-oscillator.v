module top ( out, reset );
    output reg [3:0] out;
    input reset;

    wire WB_RST;
    wire Sys_Clk0;
    // wire Sys_Clk0_Rst;

    // gclkbuff u_gclkbuff_reset ( .A(Sys_Clkdd0_Rst | WB_RST ), .Z(WB_RST_FPGA) );
    gclkbuff u_gclkbuff_clock ( .A(Sys_Clk0 | WB_RST ), .Z(WB_CLK) );

    qlal4s3b_cell_macro u_qlal4s3b_cell_macro (
        .Sys_Clk0 ( Sys_Clk0 ),
        // .Sys_Clk0_Rst ( Sys_Clk0_Rst ),
    );

    always @(posedge WB_CLK, posedge reset)
      if (reset)
          out <= 4'b0;
      else
          out <= out + 1;
endmodule
