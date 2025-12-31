package parameters;
    localparam int NODES_PER_BANK = 32;
    localparam int MESH_DIMENSION = 5;

    localparam int MAX_NODES = NODES_PER_BANK * MESH_DIMENSION * MESH_DIMENSION;
    localparam int MAX_NODES_BITS = $clog2(MAX_NODES);

    localparam int MAX_EDGES_PER_LOAD = 4;

    localparam int MAX_PATHS_BITS = MAX_NODES_BITS * MAX_EDGES_PER_LOAD;
    localparam int MAX_PATHS = 2 ** MAX_PATHS_BITS;

    localparam int MAX_EDGES_IOO = 8;

    localparam int YOU_X = 1;
    localparam int YOU_Y = 2;
    localparam int YOU_Z = 0;

    localparam int OUT_X = 3;
    localparam int OUT_Y = 2;
    localparam int OUT_Z = 0;
endpackage

package types;

    typedef enum {
        CTRL_CHILDREN,
        CTRL_PARENTS,
        CTRL_SUM,
        CTRL_START
    } ctrl_t;

    typedef struct {
        logic [MAX_NODES_BITS-1:0] node_id;
    } edge_channel_t;

    typedef union {
        typedef struct {
            logic [MAX_PATHS_BITS-1:0] value;
        } sum_t;

        typedef struct {
            edge_channel_t edges [MAX_EDGES_PER_LOAD];
            logic [$clog2(MAX_EDGES_PER_LOAD)-1:0] num_edges;
        } edges_t;  // max edges per load * max_nodes_bits + num_edges bits
    } data_u;

    typedef struct {
        logic [$clog2(MESH_DIMENSION)-1:0] x;
        logic [$clog2(MESH_DIMENSION)-1:0] y;
        logic [$clog2(NODES_PER_BANK)-1:0] z;
    } addr_t;

    typedef struct {
        addr_t addr;
        ctrl_t ctrl;
        data_u data;
    } pkt_t;
    
endpackage