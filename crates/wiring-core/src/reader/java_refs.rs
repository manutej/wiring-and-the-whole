//! Parse `// refs:` tokens from Java source (parity with scripts/extract_refs.py).

use regex::Regex;
use serde::Serialize;
use serde_json::Value;
use std::collections::{BTreeMap, BTreeSet};
use std::path::{Path, PathBuf};

#[derive(Debug, Clone, PartialEq, Eq, Serialize)]
pub struct ExtractFragment {
    pub slice: String,
    pub refs_by_file: BTreeMap<String, Vec<String>>,
    pub ref_token_count: usize,
}

/// Pure: tokens from one Java file's text (first line matching Python `REFS_LINE`).
pub fn refs_from_java_source(source: &str) -> Vec<String> {
    static RE: std::sync::OnceLock<Regex> = std::sync::OnceLock::new();
    let re = RE.get_or_init(|| Regex::new(r"//\s*refs:\s*(.+)$").expect("refs regex"));
    for line in source.lines() {
        if let Some(caps) = re.captures(line) {
            return caps[1]
                .trim()
                .split_whitespace()
                .map(str::to_string)
                .collect();
        }
    }
    vec![]
}

pub fn file_key(java_path: &Path, refs_dir: &Path) -> String {
    let rel = java_path.strip_prefix(refs_dir).unwrap_or(java_path);
    if rel.components().count() <= 1 {
        rel.file_name()
            .and_then(|n| n.to_str())
            .unwrap_or("")
            .to_string()
    } else {
        rel.to_string_lossy().replace('\\', "/")
    }
}

/// Pure over filesystem walk results: merge paths + contents into fragment.
pub fn build_fragment(
    slice: &str,
    entries: &[(String, Vec<String>)],
) -> ExtractFragment {
    let mut refs_by_file = BTreeMap::new();
    let mut ref_token_count = 0usize;
    for (key, tokens) in entries {
        ref_token_count += tokens.len();
        refs_by_file.insert(key.clone(), tokens.clone());
    }
    ExtractFragment {
        slice: slice.to_string(),
        refs_by_file,
        ref_token_count,
    }
}

pub fn walk_java_refs(refs_dir: &Path) -> Result<Vec<(String, Vec<String>)>, String> {
    if !refs_dir.is_dir() {
        return Err(format!("refs directory not found: {}", refs_dir.display()));
    }
    let mut paths: Vec<PathBuf> = Vec::new();
    walk_java_files(refs_dir, &mut paths)?;
    paths.sort();
    let mut out = Vec::new();
    for path in paths {
        let source = std::fs::read_to_string(&path).map_err(|e| e.to_string())?;
        let key = file_key(&path, refs_dir);
        let tokens = refs_from_java_source(&source);
        out.push((key, tokens));
    }
    Ok(out)
}

fn walk_java_files(dir: &Path, acc: &mut Vec<PathBuf>) -> Result<(), String> {
    for entry in std::fs::read_dir(dir).map_err(|e| e.to_string())? {
        let entry = entry.map_err(|e| e.to_string())?;
        let path = entry.path();
        if path.is_dir() {
            walk_java_files(&path, acc)?;
        } else if path.extension().is_some_and(|e| e == "java") {
            acc.push(path);
        }
    }
    Ok(())
}

pub fn fragment_to_json(fragment: &ExtractFragment) -> Result<String, String> {
    serde_json::to_string_pretty(fragment).map_err(|e| e.to_string())
}

pub fn extracted_pairs(entries: &[(String, Vec<String>)]) -> BTreeSet<(String, String)> {
    let mut out = BTreeSet::new();
    for (key, tokens) in entries {
        for token in tokens {
            out.insert((key.clone(), token.clone()));
        }
    }
    out
}

/// Pure: pairs from wiringmap v0 edge `evidence` fields (parity with `extract_refs.evidence_pairs`).
pub fn evidence_pairs_from_map(map: &Value) -> BTreeSet<(String, String)> {
    let mut covered = BTreeSet::new();
    let Some(edges) = map.get("edges").and_then(|e| e.as_array()) else {
        return covered;
    };
    for edge in edges {
        let Some(evidence) = edge.get("evidence").and_then(|e| e.as_str()) else {
            continue;
        };
        if !evidence.contains("// refs:") {
            continue;
        }
        let Some((file_part, refs_part)) = evidence.split_once("// refs:") else {
            continue;
        };
        let fname = file_part.trim().to_string();
        for token in refs_part.trim().split_whitespace() {
            covered.insert((fname.clone(), token.to_string()));
        }
    }
    covered
}

pub fn check_example_coverage(
    entries: &[(String, Vec<String>)],
    map: &Value,
) -> Result<(), String> {
    let extracted = extracted_pairs(entries);
    let covered = evidence_pairs_from_map(map);
    let mut failed = false;
    for (fname, token) in extracted.iter().filter(|p| !covered.contains(*p)) {
        failed = true;
        eprintln!("refs in witness not reflected in wiringmap example edges: {fname} -> {token}");
    }
    for (fname, token) in covered.iter().filter(|p| !extracted.contains(*p)) {
        failed = true;
        eprintln!("wiringmap example cites refs missing from witness // refs: lines: {fname} -> {token}");
    }
    if failed {
        return Err("example coverage check failed".to_string());
    }
    let edge_count = map
        .get("edges")
        .and_then(|e| e.as_array())
        .map(|a| a.len())
        .unwrap_or(0);
    let ref_token_count: usize = entries.iter().map(|(_, t)| t.len()).sum();
    eprintln!(
        "OK: {ref_token_count} ref tokens covered by {edge_count} example edges"
    );
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn parses_single_refs_line() {
        let src = "class X {}\n// refs: foo.Bar#baz other.Q#w\n";
        assert_eq!(
            refs_from_java_source(src),
            vec!["foo.Bar#baz".to_string(), "other.Q#w".to_string()]
        );
    }

    #[test]
    fn parses_whitespace_variants_like_python() {
        for src in [
            "//  refs: a.A#x\n",
            "//refs: a.A#x\n",
            "  // refs: a.A#x b.B#y  \n",
        ] {
            let got = refs_from_java_source(src);
            assert!(got.contains(&"a.A#x".to_string()), "failed on {src:?}");
        }
    }

    #[test]
    fn toybank_token_count_matches_python_golden() {
        let root = PathBuf::from(env!("CARGO_MANIFEST_DIR"))
            .join("../../witness/toybank/accounts")
            .canonicalize()
            .unwrap();
        let entries = walk_java_refs(&root).unwrap();
        let frag = build_fragment("witness/toybank/accounts", &entries);
        assert_eq!(frag.ref_token_count, 8);
    }

    #[test]
    fn fineract_thin_token_count() {
        let root = PathBuf::from(env!("CARGO_MANIFEST_DIR"))
            .join("../../fixtures/external/fineract-handlers-thin")
            .canonicalize()
            .unwrap();
        let entries = walk_java_refs(&root).unwrap();
        let frag = build_fragment("fixtures/external/fineract-handlers-thin", &entries);
        assert_eq!(frag.ref_token_count, 9);
    }

    #[test]
    fn toybank_example_coverage_passes() {
        let root = PathBuf::from(env!("CARGO_MANIFEST_DIR"))
            .join("../../witness/toybank/accounts")
            .canonicalize()
            .unwrap();
        let wm_path = PathBuf::from(env!("CARGO_MANIFEST_DIR"))
            .join("../../wiringmap/examples/toybank-accounts.v0.json")
            .canonicalize()
            .unwrap();
        let entries = walk_java_refs(&root).unwrap();
        let map: Value = serde_json::from_str(&std::fs::read_to_string(wm_path).unwrap()).unwrap();
        check_example_coverage(&entries, &map).expect("toybank example coverage");
    }
}
