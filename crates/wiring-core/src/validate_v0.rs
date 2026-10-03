//! Structural WiringMap v0 checks (Phase 1). Full JSON Schema parity via Python until toolchain catches up.

use serde::Deserialize;
use serde_json::Value;
use std::collections::HashSet;

#[derive(Debug, Deserialize)]
struct WiringMapV0 {
    schema_version: String,
    meta: Meta,
    #[serde(default)]
    junctions: Vec<Junction>,
    units: Vec<Unit>,
    edges: Vec<Edge>,
}

#[derive(Debug, Deserialize)]
struct Meta {
    repo: String,
    #[serde(rename = "ref")]
    ref_path: String,
    slice: String,
}

#[derive(Debug, Deserialize)]
struct Junction {
    id: String,
}

#[derive(Debug, Deserialize)]
struct Unit {
    id: String,
    path: String,
    role: String,
    ports: Vec<Port>,
}

#[derive(Debug, Deserialize)]
struct Port {
    id: String,
    exported: bool,
}

#[derive(Debug, Deserialize)]
struct Edge {
    id: String,
    from: String,
    to: String,
    edge_kind: String,
}

pub fn validate_v0_json(instance: &Value) -> Result<(), String> {
    let map: WiringMapV0 = serde_json::from_value(instance.clone())
        .map_err(|e| format!("wiringmap v0 shape: {e}"))?;

    if map.schema_version != "wiringmap.v0" {
        return Err(format!(
            "schema_version must be wiringmap.v0, got {}",
            map.schema_version
        ));
    }
    if map.meta.repo.is_empty() || map.meta.ref_path.is_empty() || map.meta.slice.is_empty() {
        return Err("meta.repo, meta.ref, meta.slice required".into());
    }
    if map.units.is_empty() {
        return Err("units must be non-empty".into());
    }

    let mut ids = HashSet::new();
    for j in &map.junctions {
        if !ids.insert(j.id.clone()) {
            return Err(format!("duplicate junction id {}", j.id));
        }
    }
    for u in &map.units {
        if !u.id.starts_with("unit:") {
            return Err(format!("unit id must start with unit: — {}", u.id));
        }
        if !ids.insert(u.id.clone()) {
            return Err(format!("duplicate unit id {}", u.id));
        }
        for p in &u.ports {
            if !ids.insert(p.id.clone()) {
                return Err(format!("duplicate port id {}", p.id));
            }
            let _ = p.exported;
        }
    }

    let allowed_kinds = ["call", "ref", "import", "di", "link"];
    for e in &map.edges {
        if !allowed_kinds.contains(&e.edge_kind.as_str()) {
            return Err(format!("edge {} bad edge_kind {}", e.id, e.edge_kind));
        }
        if !ids.contains(&e.from) {
            return Err(format!("edge {} from unknown endpoint {}", e.id, e.from));
        }
        if !ids.contains(&e.to) {
            return Err(format!("edge {} to unknown endpoint {}", e.id, e.to));
        }
    }

    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::fs;

    #[test]
    fn rejects_bad_version() {
        let v = serde_json::json!({
            "schema_version": "nope",
            "meta": {"repo":"r","ref":"r","slice":"s"},
            "units": [{"id":"unit:a","path":"p","role":"r","ports":[]}],
            "edges": []
        });
        assert!(validate_v0_json(&v).is_err());
    }

    #[test]
    fn golden_files() {
        let root = std::path::PathBuf::from(env!("CARGO_MANIFEST_DIR"))
            .join("../..")
            .canonicalize()
            .unwrap();
        for rel in [
            "wiringmap/examples/toybank-accounts.v0.json",
            "wiringmap/examples/repo-rust-spine.v0.json",
            "fixtures/external/fineract-handlers-thin/wiringmap.v0.json",
        ] {
            let text = fs::read_to_string(root.join(rel)).unwrap();
            let v: Value = serde_json::from_str(&text).unwrap();
            validate_v0_json(&v).unwrap_or_else(|e| panic!("{rel}: {e}"));
        }
    }
}
