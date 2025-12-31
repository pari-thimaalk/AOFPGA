module node (
    input logic clk,
    input logic rst,

    input valid_in,
    output logic ready_in,
    input pkt_t in_pkt,

    output logic valid_out,
    input ready_out,
    output pkt_t out_pkt
);
    logic you;
    logic out;

    logic [MAX_PATHS_BITS-1:0] sum_reg;
    logic [MAX_NODES_BITS-1:0] child_array [MAX_EDGES_IOO];
    logic [MAX_NODES_BITS-1:0] parent_array [MAX_EDGES_IOO];

    logic [$clog2(MAX_EDGES_IOO)-1:0] num_children, num_children_next;
    logic [$clog2(MAX_EDGES_IOO)-1:0] num_children_pending, num_children_pending_next;
    logic [$clog2(MAX_EDGES_IOO)-1:0] num_parents, num_parents_next;
    logic [MAX_EDGES_IOO-1:0] parents_pending, parents_pending_next;

    // need state to keep track of which parents have been sent to
    typedef enum logic {
        WAITING_FOR_CHILDREN,
        SENDING_TO_PARENTS
    } state_t;
    
    state_t state, state_next;

    always_ff @(posedge clk) begin
        if(rst) begin
            state <= WAITING_FOR_CHILDREN;
            sum_reg <= '0;

            num_children_pending <= '0;
            num_children <= '0;
            num_parents <= '0;
            parents_pending <= '0;

            you <= 1'b0;
            out <= 1'b0;
        end else begin
            state <= state_next;
            sum_reg <= sum_reg + ((state == WAITING_FOR_CHILDREN && valid_in && in_pkt.ctrl == CTRL_SUM) ? in_pkt.data.sum.value : '0);

            if(you == 0 && valid_in && (in_pkt.ctrl == CTRL_CHILDREN || in_pkt.ctrl == CTRL_PARENTS) && in_pkt.addr.x == YOU_X && in_pkt.addr.y == YOU_Y && in_pkt.addr. == YOU_Z) you <= 1'b1;
            if(out == 0 && valid_in && (in_pkt.ctrl == CTRL_CHILDREN || in_pkt.ctrl == CTRL_PARENTS) && in_pkt.addr.x == OUT_X && in_pkt.addr.y == OUT_Y && in_pkt.addr. == OUT_Z) you <= 1'b1;
        end
    end

    always_comb begin
        state_next = state;

        num_children_next = num_children;
        num_children_pending_next = num_children_pending;
        num_parents_next = num_parents;
        parents_pending_next = parents_pending;

        ready_in = 1'b0;
        valid_out = 1'b0;
        out_pkt = '0;

        case(state)
            WAITING_FOR_CHILDREN: begin
                ready_in = 1'b1;

                if(valid_in) begin
                    case(in_pkt.ctrl)
                        CTRL_CHILDREN: begin
                            child_array[num_children] = in_pkt.data.edges.edges[0].node_id;
                            num_children_next = num_children + 1;
                            num_children_pending_next = num_children_pending + 1;
                        end

                        CTRL_PARENTS: begin
                            parent_array[num_parents] = in_pkt.data.edges.edges[0].node_id;
                            num_parents_next = num_parents + 1;
                            parents_pending_next[num_parents] = 1'b1;
                        end

                        default: begin
                            // sum is handled in sequential block
                        end
                    endcase
                end

                if(num_children_pending_next == 0 || (out && valid_in && in_pkt.ctrl == CTRL_START)) begin
                    state_next = SENDING_TO_PARENTS;
                end
            end

            SENDING_TO_PARENTS: begin
                if(ready_out == 1'b1 && num_parents > 0) begin
                    valid_out = 1'b1;
                    out_pkt.ctrl = CTRL_SUM;
                    out_pkt.addr.x = parent_array[num_parents - 1] / (NODES_PER_BANK * MESH_DIMENSION);
                    out_pkt.addr.y = (parent_array[num_parents - 1] / NODES_PER_BANK) % MESH_DIMENSION;
                    out_pkt.addr.z = parent_array[num_parents - 1] % NODES_PER_BANK;
                    out_pkt.data.sum.value = sum_reg;

                    num_parents_next = num_parents - 1;
                end
            end
        endcase
    end
endmodule