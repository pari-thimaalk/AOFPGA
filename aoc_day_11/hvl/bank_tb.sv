module bank_tb;
    /*
    this testbench verifies one bank module, by
    confining a problem to within a single bank
    */

    timeunit 1ns;
    timeprecision 1ns;

    bit clk;
    initial clk = 1'b1;
    always #1 clk = ~clk;

    bit rst;
    task do_reset();
        rst = 1'b1;
        repeat (4) @(posedge clk);
        rst <= 1'b0;
    endtask : do_reset

    int timeout = 100;


    // logic router_valid_in;
    // logic router_ready_in;
    // pkt_t router_in_pkt;
    // logic router_valid_out;
    // logic router_ready_out;
    // pkt_t router_out_pkt;
        
    // bank dut (
    //     .clk,
    //     .rst,
    //     .router_valid_in,
    //     .router_ready_in,
    //     .router_in_pkt,
    //     .router_valid_out,
    //     .router_ready_out,
    //     .router_out_pkt
    // );

    function automatic void parse_file(input string filename);
        int fd;
        string line;
        string cur_node, children, cur_child;
        string edges[$];
        int status;

        fd = $fopen(filename, "r");
        if (fd == 0) begin
            $error("Failed to open file: %s", filename);
            return;
        end

        while (!$feof(fd)) begin
            line = "";
            status = $fgets(line, fd);

            if (status <= 0) begin
                $error("Failed to read line from file: %s", filename);
                break;
            end
            if (status == 0) break;

            cur_node = line.substr(0, 3);
            children = line.substr(4);

            // tokenize children by space
            for(int i = 0; i < children.len(); i++) begin
                if (children[i] == " ") begin
                    if (cur_child.len() > 0) begin
                        edges.push_back(cur_child);
                        cur_child = "";
                    end
                end else begin
                    cur_child = {cur_child, children.getc(i)};
                end
            end

            edges.push_back(cur_child); cur_child = ""; // add last child

            // Process the line as needed
            $display("Read line: %s", line);
            $display("Current Node: %s", cur_node);
            foreach (edges[i]) begin
                $display("  Edge to: %s", edges[i]);
            end
            edges.delete();
        end
    endfunction
        
    initial begin
        $fsdbDumpfile("dump.fsdb");
        $fsdbDumpvars(0, "+all");
        // do_reset();
        void'($system("pwd"));
        parse_file("../../testcases/small_input.txt");
        $finish;
    end

endmodule