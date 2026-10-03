use clap::Parser;
use std::path::PathBuf;
use wiring_core::pack::run_reexpand_gate;

#[derive(Parser)]
#[command(
    name = "wiring-reexpand",
    about = "Byte gate: factored pack re-expansion (parity with scripts/reexpand_gate.py)"
)]
struct Args {
    /// Directory containing pack_explicit.txt, pack_factored.txt, and LEGEND.txt
    pack_dir: PathBuf,

    /// Canonical E2 pack legend for LEGEND.txt check
    #[arg(
        long,
        default_value = "experiments/e2-tokens/pack_LEGEND.txt"
    )]
    canonical_legend: PathBuf,
}

fn main() {
    let args = Args::parse();
    let pack_dir = args.pack_dir.canonicalize().unwrap_or_else(|e| {
        eprintln!("FAIL: pack_dir: {e}");
        std::process::exit(1);
    });
    let canonical = std::fs::read_to_string(&args.canonical_legend).unwrap_or_else(|e| {
        eprintln!("FAIL: canonical legend: {e}");
        std::process::exit(1);
    });
    match run_reexpand_gate(&pack_dir, &canonical) {
        Ok(()) => {
            println!("PASS reexpand gate ({})", pack_dir.display());
        }
        Err(msg) => {
            eprintln!("FAIL reexpand gate ({}): {msg}", pack_dir.display());
            std::process::exit(1);
        }
    }
}
