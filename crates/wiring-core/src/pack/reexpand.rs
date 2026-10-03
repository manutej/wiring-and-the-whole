//! Re-expand factored L2 pack rows (parity with scripts/reexpand_gate.py).

use regex::Regex;
use std::path::Path;

pub fn normalize_text(text: &str) -> String {
    if text.ends_with('\n') {
        text.to_string()
    } else {
        format!("{text}\n")
    }
}

pub fn validate_legend(pack_dir: &Path, canonical_legend: &str) -> Result<(), String> {
    let legend_path = pack_dir.join("LEGEND.txt");
    if !legend_path.is_file() {
        return Err(format!("FAIL: missing {}", legend_path.display()));
    }
    let legend = std::fs::read_to_string(&legend_path).map_err(|e| e.to_string())?;
    if normalize_text(&legend) != normalize_text(canonical_legend) {
        return Err(
            "FAIL reexpand gate: LEGEND.txt must match canonical E2 pack legend \
             (experiments/e2-tokens/pack_LEGEND.txt)"
                .to_string(),
        );
    }
    Ok(())
}

pub fn expand_slice_unit_row(row: &str) -> Result<Vec<String>, String> {
    static RE: std::sync::OnceLock<Regex> = std::sync::OnceLock::new();
    let re = RE.get_or_init(|| {
        Regex::new(r"inst SliceUnit\((\w+), edges=\[(.*)\]\)\s*$").expect("slice regex")
    });
    let caps = re
        .captures(row.trim())
        .ok_or_else(|| format!("bad SliceUnit inst row: {row:?}"))?;
    let unit = caps[1].to_string();
    let mut edges: Vec<&str> = caps[2]
        .split(',')
        .map(str::trim)
        .filter(|s| !s.is_empty())
        .collect();
    edges.sort();
    let mut lines = vec![format!("unit {unit}")];
    for target in edges {
        lines.push(format!("edge {unit} -> {target}"));
    }
    Ok(lines)
}

pub fn expand_command_handler_row(row: &str) -> Result<Vec<String>, String> {
    let stripped = row.trim();
    static RE6: std::sync::OnceLock<Regex> = std::sync::OnceLock::new();
    static RE5: std::sync::OnceLock<Regex> = std::sync::OnceLock::new();
    let re6 = RE6.get_or_init(|| {
        Regex::new(
            r"inst CommandHandler\((\w+),\s*(\w+),\s*(\w+),\s*(\w+),\s*(\w+),\s*(\w+)\)\s*$",
        )
        .expect("ch6")
    });
    if let Some(c) = re6.captures(stripped) {
        return Ok(vec![
            format!("unit {}", &c[1]),
            format!(
                "anno {} @CommandType entity={} action={}",
                &c[1], &c[5], &c[6]
            ),
            format!("dep {}.{}: {}", &c[1], &c[2], &c[3]),
            format!("edge {} -> {}#{}", &c[1], &c[3], &c[4]),
        ]);
    }
    let re5 = RE5.get_or_init(|| {
        Regex::new(r"inst CommandHandler\((\w+),\s*(\w+),\s*(\w+),\s*(\w+),\s*(\w+)\)\s*$")
            .expect("ch5")
    });
    let c = re5
        .captures(stripped)
        .ok_or_else(|| format!("bad CommandHandler inst row: {row:?}"))?;
    Ok(vec![
        format!("unit {}", &c[1]),
        format!(
            "anno {} @CommandType entity={} action={}",
            &c[1], &c[4], &c[5]
        ),
        format!("dep {}.writePlatformService: {}", &c[1], &c[2]),
        format!("edge {} -> {}#{}", &c[1], &c[2], &c[3]),
    ])
}

pub fn expand_inst_row(row: &str) -> Result<Vec<String>, String> {
    let stripped = row.trim();
    if stripped.starts_with("inst CommandHandler(") {
        return expand_command_handler_row(row);
    }
    if stripped.starts_with("inst SliceUnit(") {
        return expand_slice_unit_row(row);
    }
    Err(format!("unknown inst row: {row:?}"))
}

pub fn expand_factored(factored_text: &str) -> Result<String, String> {
    let mut lines: Vec<String> = Vec::new();
    for raw in factored_text.lines() {
        let line = raw.trim();
        if line.is_empty() || line.starts_with("motif ") || line.starts_with("foreach ") {
            continue;
        }
        if line.starts_with("inst ") {
            lines.extend(expand_inst_row(line)?);
        }
    }
    Ok(format!("{}\n", lines.join("\n")))
}

pub fn run_reexpand_gate(pack_dir: &Path, canonical_legend: &str) -> Result<(), String> {
    let explicit_path = pack_dir.join("pack_explicit.txt");
    let factored_path = pack_dir.join("pack_factored.txt");
    for p in [&explicit_path, &factored_path] {
        if !p.is_file() {
            return Err(format!("FAIL: missing {}", p.display()));
        }
    }
    let explicit = std::fs::read_to_string(&explicit_path).map_err(|e| e.to_string())?;
    let factored = std::fs::read_to_string(&factored_path).map_err(|e| e.to_string())?;
    validate_legend(pack_dir, canonical_legend)?;
    let reexpanded = expand_factored(&factored)?;
    if reexpanded == explicit {
        Ok(())
    } else {
        Err("factored expansion != pack_explicit.txt".into())
    }
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
    fn toybank_pack_reexpand() {
        let root = repo_root();
        let pack = root.join("wiringmap/examples/toybank-accounts.v0.pack");
        let legend =
            std::fs::read_to_string(root.join("experiments/e2-tokens/pack_LEGEND.txt")).unwrap();
        run_reexpand_gate(&pack, &legend).expect("toybank pack");
    }

    #[test]
    fn rejects_tampered_legend() {
        let root = repo_root();
        let pack = root.join("wiringmap/examples/toybank-accounts.v0.pack");
        let err = run_reexpand_gate(&pack, "not canonical\n").unwrap_err();
        assert!(err.contains("LEGEND.txt must match"));
    }

    #[test]
    fn command_handler_five_arg() {
        let row = "inst CommandHandler(H, Svc, meth, ENT, ACT)";
        let got = expand_inst_row(row).unwrap();
        assert_eq!(got[2], "dep H.writePlatformService: Svc");
    }
}
