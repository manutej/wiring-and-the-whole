use clap::Parser;
use std::path::PathBuf;
use wiring_core::pack::{build_l2_pack_files, pack_dir_for_map, write_l2_pack};

#[derive(Parser)]
#[command(
    name = "wiring-build-l2-pack",
    about = "Build L2 pack v0 from wiringmap JSON (parity with scripts/build_l2_pack.py)"
)]
struct Args {
    /// wiringmap.v0 JSON path
    #[arg(default_value = "wiringmap/examples/toybank-accounts.v0.json")]
    input: PathBuf,

    /// Output stem (default: <input json stem>; writes <stem>.pack/)
    #[arg(long)]
    out: Option<PathBuf>,

    /// Canonical E2 pack legend copied into LEGEND.txt
    #[arg(
        long,
        default_value = "experiments/e2-tokens/pack_LEGEND.txt"
    )]
    canonical_legend: PathBuf,
}

fn main() {
    let args = Args::parse();
    let input = args.input.canonicalize().unwrap_or_else(|e| {
        eprintln!("FAIL: input: {e}");
        std::process::exit(1);
    });
    let out_dir = pack_dir_for_map(
        &input,
        args.out.as_deref(),
    );

    let artifacts = build_l2_pack_files(&input, &args.canonical_legend).unwrap_or_else(|e| {
        eprintln!("FAIL build l2 pack: {e}");
        std::process::exit(1);
    });

    write_l2_pack(&out_dir, &artifacts).unwrap_or_else(|e| {
        eprintln!("FAIL write pack: {e}");
        std::process::exit(1);
    });

    println!(
        "wrote {}/LEGEND.txt pack_explicit.txt pack_factored.txt",
        out_dir.display()
    );
}
