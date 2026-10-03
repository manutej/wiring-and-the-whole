use clap::Parser;
use std::path::PathBuf;
use wiring_core::reader::java_refs::{build_fragment, fragment_to_json, walk_java_refs};

#[derive(Parser)]
#[command(name = "wiring-extract-java-refs", about = "Extract // refs: from Java tree (JSON stdout)")]
struct Args {
    /// Directory of *.java files (default: witness/toybank/accounts)
    refs_dir: Option<PathBuf>,

    /// Slice label in JSON (default: relative path from cwd)
    #[arg(long)]
    slice: Option<String>,
}

fn main() {
    let args = Args::parse();
    let refs_dir = args
        .refs_dir
        .unwrap_or_else(|| PathBuf::from("witness/toybank/accounts"));

    let refs_dir = if refs_dir.is_absolute() {
        refs_dir
    } else {
        std::env::current_dir()
            .unwrap_or_else(|_| PathBuf::from("."))
            .join(refs_dir)
    };

    let slice = args.slice.unwrap_or_else(|| {
        refs_dir
            .strip_prefix(std::env::current_dir().unwrap_or_else(|_| PathBuf::from(".")))
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
}
