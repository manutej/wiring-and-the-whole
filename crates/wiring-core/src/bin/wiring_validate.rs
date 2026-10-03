use clap::Parser;
use std::path::PathBuf;
use wiring_core::validate_files;

#[derive(Parser)]
#[command(name = "wiring-validate", about = "Validate WiringMap v0 JSON against schema")]
struct Args {
    /// Path to wiringmap/schema.v0.json
    #[arg(long, default_value = "wiringmap/schema.v0.json")]
    schema: PathBuf,

    /// Path to a WiringMap v0 instance
    #[arg(long, default_value = "wiringmap/examples/toybank-accounts.v0.json")]
    instance: PathBuf,
}

fn main() {
    let args = Args::parse();
    match validate_files(&args.schema, &args.instance) {
        Ok(()) => {
            println!(
                "OK: {} validates against {}",
                args.instance.display(),
                args.schema.file_name().unwrap_or_default().to_string_lossy()
            );
        }
        Err(msg) => {
            eprintln!("validation failed: {msg}");
            std::process::exit(1);
        }
    }
}
