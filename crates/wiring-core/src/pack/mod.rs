//! L2 pack re-expansion (parity with scripts/reexpand_gate.py).

pub mod reexpand;

pub use reexpand::{
    expand_command_handler_row, expand_factored, expand_inst_row, expand_slice_unit_row,
    normalize_text, run_reexpand_gate, validate_legend,
};
