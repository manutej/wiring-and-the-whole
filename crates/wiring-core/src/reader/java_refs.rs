//! Parse `// refs:` tokens from Java source (parity with scripts/extract_refs.py).

use serde::Serialize;
use std::collections::BTreeMap;
use std::path::{Path, PathBuf};

#[derive(Debug, Clone, PartialEq, Eq, Serialize)]
pub struct ExtractFragment {
    pub slice: String,
    pub refs_by_file: BTreeMap<String, Vec<String>>,
    pub ref_token_count: usize,
}

/// Pure: tokens from one Java file's text.
pub fn refs_from_java_source(source: &str) -> Vec<String> {
    let mut tokens = Vec::new();
    for line in source.lines() {
        if let Some(rest) = line.split("// refs:").nth(1) {
            tokens.extend(
                rest.trim()
                    .split_whitespace()
                    .map(str::to_string)
                    .collect::<Vec<_>>(),
            );
            break;
        }
    }
    tokens
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
}
