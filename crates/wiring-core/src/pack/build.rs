//! Build L2 pack v0 from wiringmap.v0 JSON (parity with scripts/build_l2_pack.py).

use serde_json::Value;
use std::collections::{BTreeMap, BTreeSet};
use std::path::{Path, PathBuf};

use super::reexpand::{expand_factored, normalize_text};

pub const MOTIF_SLICE_UNIT: &str = "motif SliceUnit(U, edges):
  unit $U
  foreach E in $edges -> edge $U -> $E
";

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct L2PackArtifacts {
    pub legend: String,
    pub explicit: String,
    pub factored: String,
}

pub fn short_unit(unit_id: &str) -> String {
    if let Some(rest) = unit_id.strip_prefix("unit:") {
        rest.rsplit('.').next().unwrap_or(rest).to_string()
    } else {
        unit_id.to_string()
    }
}

pub fn port_unit_symbol(port_id: &str) -> Result<(String, String), String> {
    let body = port_id
        .strip_prefix("port:")
        .ok_or_else(|| format!("unsupported port id {port_id:?}"))?;
    let (unit_part, sym) = body
        .split_once('#')
        .ok_or_else(|| format!("port missing # symbol: {port_id:?}"))?;
    let short = unit_part
        .rsplit('.')
        .next()
        .unwrap_or(unit_part)
        .to_string();
    Ok((short, sym.to_string()))
}

fn junction_target(junction: &Value) -> Result<String, String> {
    junction
        .get("label")
        .and_then(|v| v.as_str())
        .map(str::to_string)
        .ok_or_else(|| "junction missing label".to_string())
}

pub fn edge_target(
    edge: &Value,
    junctions: &BTreeMap<String, Value>,
) -> Result<(String, String), String> {
    let from = edge
        .get("from")
        .and_then(|v| v.as_str())
        .ok_or_else(|| "edge missing from".to_string())?;
    let from_u = if from.starts_with("port:") {
        port_unit_symbol(from)?.0
    } else if from.starts_with("unit:") {
        short_unit(from)
    } else {
        return Err(format!("unsupported edge.from {from:?}"));
    };

    let to = edge
        .get("to")
        .and_then(|v| v.as_str())
        .ok_or_else(|| "edge missing to".to_string())?;
    let target = if to.starts_with("port:") {
        let (to_u, sym) = port_unit_symbol(to)?;
        format!("{to_u}#{sym}")
    } else if to.starts_with("junction:") {
        let junction = junctions
            .get(to)
            .ok_or_else(|| format!("unknown junction {to:?}"))?;
        junction_target(junction)?
    } else if to.starts_with("unit:") {
        short_unit(to)
    } else {
        return Err(format!("unsupported edge.to {to:?}"));
    };

    Ok((from_u, target))
}

pub fn collect_unit_edges(wm: &Value) -> Result<BTreeMap<String, Vec<String>>, String> {
    let units = wm
        .get("units")
        .and_then(|v| v.as_array())
        .ok_or_else(|| "wiringmap missing units array".to_string())?;

    let mut junctions: BTreeMap<String, Value> = BTreeMap::new();
    if let Some(arr) = wm.get("junctions").and_then(|v| v.as_array()) {
        for j in arr {
            let id = j
                .get("id")
                .and_then(|v| v.as_str())
                .ok_or_else(|| "junction missing id".to_string())?;
            junctions.insert(id.to_string(), j.clone());
        }
    }

    let mut by_unit: BTreeMap<String, BTreeSet<String>> = BTreeMap::new();
    for u in units {
        let id = u
            .get("id")
            .and_then(|v| v.as_str())
            .ok_or_else(|| "unit missing id".to_string())?;
        by_unit.entry(short_unit(id)).or_default();
    }

    if let Some(edges) = wm.get("edges").and_then(|v| v.as_array()) {
        for edge in edges {
            let (from_u, target) = edge_target(edge, &junctions)?;
            by_unit.entry(from_u).or_default().insert(target);
        }
    }

    Ok(by_unit
        .into_iter()
        .map(|(u, targets)| (u, targets.into_iter().collect()))
        .collect())
}

pub fn explicit_lines(unit_edges: &BTreeMap<String, Vec<String>>) -> String {
    let mut lines: Vec<String> = Vec::new();
    for unit in unit_edges.keys() {
        lines.push(format!("unit {unit}"));
        if let Some(targets) = unit_edges.get(unit) {
            for target in targets {
                lines.push(format!("edge {unit} -> {target}"));
            }
        }
    }
    normalize_text(&lines.join("\n"))
}

pub fn factored_lines(unit_edges: &BTreeMap<String, Vec<String>>) -> String {
    let mut parts: Vec<String> = vec![MOTIF_SLICE_UNIT.trim_end().to_string(), String::new()];
    for unit in unit_edges.keys() {
        let edges = unit_edges.get(unit).map(Vec::as_slice).unwrap_or(&[]);
        if edges.is_empty() {
            parts.push(format!("inst SliceUnit({unit}, edges=[])"));
        } else {
            let edge_list = edges.join(",");
            parts.push(format!("inst SliceUnit({unit}, edges=[{edge_list}])"));
        }
    }
    normalize_text(&parts.join("\n"))
}

pub fn build_l2_pack_from_wiringmap(
    wm: &Value,
    canonical_legend: &str,
) -> Result<L2PackArtifacts, String> {
    let unit_edges = collect_unit_edges(wm)?;
    let explicit = explicit_lines(&unit_edges);
    let factored = factored_lines(&unit_edges);
    let legend = normalize_text(canonical_legend);

    let reexpanded = expand_factored(&factored)?;
    if reexpanded != explicit {
        return Err("internal error: expand(factored) != explicit".to_string());
    }

    Ok(L2PackArtifacts {
        legend,
        explicit,
        factored,
    })
}

pub fn build_l2_pack_files(
    wiringmap_path: &Path,
    canonical_legend_path: &Path,
) -> Result<L2PackArtifacts, String> {
    let text = std::fs::read_to_string(wiringmap_path)
        .map_err(|e| format!("wiringmap read failed: {e}"))?;
    let wm: Value = serde_json::from_str(&text).map_err(|e| format!("wiringmap json: {e}"))?;
    let legend = std::fs::read_to_string(canonical_legend_path)
        .map_err(|e| format!("legend read failed: {e}"))?;
    build_l2_pack_from_wiringmap(&wm, &legend)
}

pub fn pack_dir_for_map(wiringmap_path: &Path, out_stem: Option<&Path>) -> PathBuf {
    let stem = out_stem
        .map(Path::to_path_buf)
        .unwrap_or_else(|| wiringmap_path.with_extension(""));
    PathBuf::from(format!("{}.pack", stem.display()))
}

pub fn write_l2_pack(out_dir: &Path, artifacts: &L2PackArtifacts) -> Result<(), String> {
    std::fs::create_dir_all(out_dir).map_err(|e| e.to_string())?;
    std::fs::write(out_dir.join("LEGEND.txt"), &artifacts.legend).map_err(|e| e.to_string())?;
    std::fs::write(out_dir.join("pack_explicit.txt"), &artifacts.explicit)
        .map_err(|e| e.to_string())?;
    std::fs::write(out_dir.join("pack_factored.txt"), &artifacts.factored)
        .map_err(|e| e.to_string())?;
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::path::PathBuf;

    fn repo_root() -> PathBuf {
        PathBuf::from(env!("CARGO_MANIFEST_DIR"))
            .join("../..")
            .canonicalize()
            .expect("repo root")
    }

    #[test]
    fn toybank_build_matches_python_golden() {
        let root = repo_root();
        let wm_path = root.join("wiringmap/examples/toybank-accounts.v0.json");
        let legend_path = root.join("experiments/e2-tokens/pack_LEGEND.txt");
        let py_pack = root.join("wiringmap/examples/toybank-accounts.v0.pack");

        let artifacts = build_l2_pack_files(&wm_path, &legend_path).expect("build");

        let py_explicit =
            std::fs::read_to_string(py_pack.join("pack_explicit.txt")).expect("py explicit");
        let py_factored =
            std::fs::read_to_string(py_pack.join("pack_factored.txt")).expect("py factored");
        let py_legend = std::fs::read_to_string(py_pack.join("LEGEND.txt")).expect("py legend");

        assert_eq!(artifacts.explicit, py_explicit);
        assert_eq!(artifacts.factored, py_factored);
        assert_eq!(artifacts.legend, normalize_text(&py_legend));
    }
}
