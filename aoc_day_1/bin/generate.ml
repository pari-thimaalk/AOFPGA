open! Core
open! Hardcaml
open! Aoc_1

let generate_zero_ctr_rtl () =
  let module C = Circuit.With_interface (Zero_ctr.I) (Zero_ctr.O) in
  let scope = Scope.create ~auto_label_hierarchical_ports:true () in
  let circuit = C.create_exn ~name:"zero_ctr_top" (Zero_ctr.hierarchical scope) in
  let rtl_circuits =
    Rtl.create ~database:(Scope.circuit_database scope) Verilog [ circuit ]
  in
  let rtl = Rtl.full_hierarchy rtl_circuits |> Rope.to_string in
  print_endline rtl
;;

let zero_ctr_rtl_command =
  Command.basic
    ~summary:""
    [%map_open.Command
      let () = return () in
      fun () -> generate_zero_ctr_rtl ()]
;;

let () =
  Command_unix.run
    (Command.group ~summary:"" [ "zero-ctr", zero_ctr_rtl_command ])
;;