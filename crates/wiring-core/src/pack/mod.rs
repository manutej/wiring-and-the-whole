//! L2 pack build and re-expansion (parity with scripts/build_l2_pack.py / reexpand_gate.py).

pub mod build;
pub mod reexpand;

pub use build::{
    build_l2_pack_files, build_l2_pack_from_wiringmap, collect_unit_edges, pack_dir_for_map,
    explicit_lines, factored_lines, write_l2_pack, L2PackArtifacts, MOTIF_SLICE_UNIT,
};
pub use reexpand::{
    expand_command_handler_row, expand_factored, expand_inst_row, expand_slice_unit_row,
    normalize_text, run_reexpand_gate, validate_legend,
};
