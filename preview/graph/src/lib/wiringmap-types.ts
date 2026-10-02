export type WiringMapV0 = {
  schema_version: string;
  meta: { repo: string; ref: string; slice: string; notes?: string };
  junctions: Array<{
    id: string;
    label: string;
    junction_kind: string;
  }>;
  units: Array<{
    id: string;
    path: string;
    role: string;
    ports: Array<{ id: string; symbol: string; kind: string }>;
  }>;
  edges: Array<{
    id: string;
    from: string;
    to: string;
    edge_kind: string;
    evidence?: string;
  }>;
};
