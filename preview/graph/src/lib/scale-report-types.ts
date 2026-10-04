export type ScaleReportV0 = {
  schema_version: "scale-report.v0";
  generated_at_utc: string;
  git_sha: string;
  corpus: {
    kind: string;
    summary: string;
    upstream_repo: string;
    upstream_commit_pinned: boolean;
    source_pools?: string[];
  };
  metrics: {
    slice_matrix_slices: number;
    matrix_unique_java_loc: number;
    edge_recall_frozen_pairs: number;
    edge_recall_distinct_pairs: number;
    charter_10k?: { loc: number; java_files: number; ref_tokens: number };
  };
  charter_10k_breakdown: {
    handler_loc: number;
    context_loc: number;
    handler_java_files: number;
    context_java_files: number;
    mapped_fraction_loc: number;
    wiringmap_units: number;
    wiringmap_edges: number;
  };
  performance?: {
    matrix_total_ms_rust?: number;
    matrix_total_ms_python?: number;
    charter_10k_total_ms?: number;
    charter_10k_extract_ms?: number;
  };
  representation_compare?: {
    tokens_factored?: number;
    tokens_ast?: number;
    tokens_raw?: number;
    pass_l2_factored?: number;
    pass_l2_md?: number;
    pass_ast?: number;
  };
  slice_matrix_timing: {
    rust: {
      total_ms: number;
      slices: Array<{
        id: string;
        java_files: number;
        steps_ms: {
          validate_ms: number;
          extract_ms: number;
          pack_ms: number;
          reexpand_ms: number;
          total_ms: number;
        };
      }>;
    };
    python: { total_ms: number };
  };
  viewing: {
    comprehensive_wiring_mermaid: string;
    html_dashboard: string;
  };
};
