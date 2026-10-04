/** Mermaid sources for scale / compound-build views (also mirrored in docs/SCALE-DIAGRAMS.md). */

export const compoundProgrammeDag = `flowchart TB
  subgraph setup [Setup]
    P[Programme checklist]
    B[Integration branch]
    S[Build specs per slice]
  end
  subgraph slices [Slice loop]
    BL[Builder spec only]
    IM[Implement commit push]
    GT[Gates pulse-loop]
    EV[Independent SHIP]
  end
  subgraph ship [Ship once]
    PR[Single integration PR]
    MG[Merge]
  end
  setup --> slices
  slices --> slices
  slices --> ship`;

export const sliceMatrixDag = `flowchart LR
  M[manifest.v0.json]
  subgraph shards [Parallel CI shards]
    S1[toybank accounts]
    S2[toybank loans]
    S3[toybank savings]
    S4[fineract thin]
    S5[charter 1k]
    S6[report module]
    S7[charter 10k]
  end
  R[Reducer JSON report]
  M --> S1 & S2 & S3 & S4 & S5 & S6 & S7
  S1 & S2 & S3 & S4 & S5 & S6 & S7 --> R`;

export const scaleLadderDag = `flowchart TB
  M0[M0 demo verify pipeline preview]
  M1[M1 Rust engine parity]
  M2[M2 charter 1k plus recall 125]
  S2[S2 slice matrix 7 shards]
  S3[S3 scale metrics plus diagrams]
  M3[M3 charter 10k scale test]
  M0 --> M1 --> M2 --> S2 --> S3 --> M3`;

export const wiringMathDag = `flowchart TB
  subgraph wiring [Wiring gates]
    E[extract refs]
    WM[WiringMap evidence]
    P[L2 pack]
    X[reexpand bytes]
  end
  subgraph math [Math gates]
    T[token report WIN]
    N[n star breakeven]
    L[LOC charter bounds]
  end
  E --> WM --> P --> X
  T --> N
  L --> WM`;

export const rustPipelineSeq = `sequenceDiagram
  participant CI as make slice-matrix-check
  participant R as wiring-core CLI
  participant Py as Python fallback
  CI->>R: WIRING_ENGINE=rust validate extract pack reexpand
  R-->>CI: per-shard OK
  Note over CI,Py: extract example check Rust or Python parity`;
