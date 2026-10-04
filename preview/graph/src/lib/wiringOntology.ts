/** Fineract-oriented ontological buckets for handler / platform clustering. */
export type OntologyGroupId =
  | "loan"
  | "savings"
  | "client"
  | "org"
  | "infra"
  | "other";

export type OntologyGroup = {
  id: OntologyGroupId;
  label: string;
  kicker: string;
  patterns: RegExp[];
};

export const WIRING_ONTOLOGY_GROUPS: OntologyGroup[] = [
  {
    id: "loan",
    label: "Loan lifecycle",
    kicker: "disburse · repay · charges",
    patterns: [
      /loan/i,
      /disburse/i,
      /repay/i,
      /foreclos/i,
      /reschedule/i,
      /charge/i,
      /delinquency/i,
      /creditbalance/i,
    ],
  },
  {
    id: "savings",
    label: "Savings & shares",
    kicker: "accounts · deposits",
    patterns: [/savings/i, /deposit/i, /fixed/i, /share/i, /activate/i],
  },
  {
    id: "client",
    label: "Clients & groups",
    kicker: "GLIM · originators",
    patterns: [/client/i, /glim/i, /group/i, /center/i, /originator/i, /bulkupdate/i],
  },
  {
    id: "org",
    label: "Organisation",
    kicker: "office · staff · products",
    patterns: [/office/i, /staff/i, /holiday/i, /currency/i, /paymenttype/i, /fund/i, /product/i],
  },
  {
    id: "infra",
    label: "Command substrate",
    kicker: "JsonCommand · integrity",
    patterns: [/jsoncommand/i, /dataintegrity/i, /commandhandler/i, /processcommand/i],
  },
  {
    id: "other",
    label: "Other",
    kicker: "unclassified",
    patterns: [],
  },
];

const GROUP_BY_ID = new Map(WIRING_ONTOLOGY_GROUPS.map((g) => [g.id, g]));

export function ontologyGroupMeta(id: OntologyGroupId): OntologyGroup {
  return GROUP_BY_ID.get(id) ?? WIRING_ONTOLOGY_GROUPS[WIRING_ONTOLOGY_GROUPS.length - 1]!;
}

export function inferOntologyFromText(text: string): OntologyGroupId {
  for (const g of WIRING_ONTOLOGY_GROUPS) {
    if (g.id === "other") continue;
    if (g.patterns.some((p) => p.test(text))) return g.id;
  }
  return "other";
}

/** Stalks-and-sections hierarchy planes for wiring maps. */
export const WIRING_LEVELS = [
  {
    id: 0,
    code: "L0",
    label: "Command substrate",
    kicker: "shared infra",
    blurb: "JsonCommand, integrity handlers — bottom glass plane.",
  },
  {
    id: 1,
    code: "L1",
    label: "Platform stalks",
    kicker: "glued services",
    blurb: "WritePlatform / repository junctions — restriction targets.",
  },
  {
    id: 2,
    code: "L2",
    label: "Handler sections",
    kicker: "wired units",
    blurb: "@CommandType handlers clustered by domain.",
  },
] as const;

export function layerToLevel(layer: "handler" | "service" | "infra"): number {
  switch (layer) {
    case "infra":
      return 0;
    case "service":
      return 1;
    case "handler":
      return 2;
    default: {
      const _exhaustive: never = layer;
      return _exhaustive;
    }
  }
}

export function levelHue(level: number): string {
  const hues = ["#6d6a55", "#009465", "#c23b22"];
  return hues[Math.min(level, hues.length - 1)] ?? "#253122";
}

export function ontologyAccent(id: OntologyGroupId): string {
  switch (id) {
    case "loan":
      return "#c23b22";
    case "savings":
      return "#009465";
    case "client":
      return "#501345";
    case "org":
      return "#9a72aa";
    case "infra":
      return "#6d6a55";
    case "other":
      return "#253122";
    default: {
      const _exhaustive: never = id;
      return _exhaustive;
    }
  }
}
