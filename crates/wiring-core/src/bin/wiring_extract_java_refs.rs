use clap::Parser;
use std::path::PathBuf;
use wiring_core::reader::java_refs::{
    build_fragment, check_example_coverage, fragment_to_json, walk_java_refs,
};

#[derive(Parser)]
#[command(name = "wiring-extract-java-refs", about = "Extract // refs: from Java tree (JSON stdout)")]
struct Args {
    /// Directory of *.java files (default: witness/toybank/accounts)
    refs_dir: Option<PathBuf>,

    /// Slice label in JSON (default: relative path from cwd)
    #[arg(long)]
    slice: Option<String>,

    /// WiringMap v0 JSON for coverage check (parity with extract_refs.py --example)
    #[arg(long)]
    example: Option<PathBuf>,

    /// Skip wiringmap edge coverage (parity with --no-example-check)
    #[arg(long)]
    no_example_check: bool,
}

fn main() {
    let args = Args::parse();
    let cwd = std::env::current_dir().unwrap_or_else(|_| PathBuf::from("."));
    let refs_dir = args
        .refs_dir
        .unwrap_or_else(|| PathBuf::from("witness/toybank/accounts"));

    let refs_dir = if refs_dir.is_absolute() {
        refs_dir
    } else {
        cwd.join(refs_dir)
    };

    let slice = args.slice.unwrap_or_else(|| {
        refs_dir
            .strip_prefix(&cwd)
            .map(|p| p.to_string_lossy().replace('\\', "/"))
            .unwrap_or_else(|_| refs_dir.to_string_lossy().into_owned())
    });

    let entries = match walk_java_refs(&refs_dir) {
        Ok(e) => e,
        Err(msg) => {
            eprintln!("ERROR: {msg}");
            std::process::exit(1);
        }
    };
    let fragment = build_fragment(&slice, &entries);
    match fragment_to_json(&fragment) {
        Ok(json) => println!("{json}"),
        Err(msg) => {
            eprintln!("ERROR: {msg}");
            std::process::exit(1);
        }
    }

    if args.no_example_check {
        eprintln!(
            "OK: {} ref tokens extracted (no wiringmap example check)",
            fragment.ref_token_count
        );
        return;
    }

    let example_path = match args.example {
        Some(p) if p.is_absolute() => p,
        Some(p) => cwd.join(p),
        None => cwd.join("wiringmap/examples/toybank-accounts.v0.json"),
    };

    if !example_path.is_file() {
        eprintln!("ERROR: missing example instance: {}", example_path.display());
        std::process::exit(1);
    }

    let map_text = match std::fs::read_to_string(&example_path) {
        Ok(t) => t,
        Err(e) => {
            eprintln!("ERROR: read example: {e}");
            std::process::exit(1);
        }
    };
    let map: serde_json::Value = match serde_json::from_str(&map_text) {
        Ok(v) => v,
        Err(e) => {
            eprintln!("ERROR: parse wiringmap JSON: {e}");
            std::process::exit(1);
        }
    };

    if let Err(msg) = check_example_coverage(&entries, &map) {
        eprintln!("{msg}");
        std::process::exit(1);
    }
}
