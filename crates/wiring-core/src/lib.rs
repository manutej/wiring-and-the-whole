//! WiringMap v0 core — validate and typed graph IR (Phase 1).

mod validate_v0;

use serde_json::Value;
use std::path::Path;
pub use validate_v0::validate_v0_json;

pub fn validate_instance(_schema: &Value, instance: &Value) -> Result<(), String> {
    validate_v0_json(instance)
}

pub fn validate_files(schema_path: &Path, instance_path: &Path) -> Result<(), String> {
    let _schema_text = std::fs::read_to_string(schema_path)
        .map_err(|e| format!("schema read failed: {e}"))?;
    let instance_text = std::fs::read_to_string(instance_path)
        .map_err(|e| format!("instance read failed: {e}"))?;
    let instance: Value =
        serde_json::from_str(&instance_text).map_err(|e| format!("instance json: {e}"))?;
    validate_v0_json(&instance)
}

#[cfg(test)]
mod integration {
    use super::*;
    use std::path::PathBuf;

    fn repo_root() -> PathBuf {
        PathBuf::from(env!("CARGO_MANIFEST_DIR"))
            .join("../..")
            .canonicalize()
            .expect("repo root")
    }

    #[test]
    fn toybank_map_validates() {
        let root = repo_root();
        let schema = root.join("wiringmap/schema.v0.json");
        let instance = root.join("wiringmap/examples/toybank-accounts.v0.json");
        validate_files(&schema, &instance).expect("toybank validates");
    }
}
