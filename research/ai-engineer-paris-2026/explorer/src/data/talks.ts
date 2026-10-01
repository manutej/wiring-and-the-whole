export type VizKind =
  | 'deep-module'
  | 'review-gate'
  | 'eval-loop'
  | 'factory-line'
  | 'enterprise-stack'
  | 'orchestra'
  | 'survey-radar'

export type Talk = {
  slug: string
  videoId: string
  title: string
  speaker: string
  org: string
  accent: string
  metaphor: string
  thesis: string
  hook: string
  durationMin: number
  transcriptWords: number
  stats: { value: string; label: string; cite?: string }[]
  symbols: { term: string; meaning: string }[]
  vocab: { term: string; def: string; viz: VizKind }[]
  failureModes: { title: string; body: string }[]
  demoStages: { label: string; meta: string }[]
  diagram: 'pr-pipeline' | 'review-cliff' | 'factory-loop' | 'build-buy' | 'orchestra-pit' | 'dx-radar'
}

export const talks: Talk[] = [
  {
    slug: 'pr-bottleneck',
    videoId: 'LlgiOCmFG_w',
    title: 'Fixing the PR Bottleneck',
    speaker: 'Matt Pocock',
    org: 'AIHero',
    accent: '#f59e0b',
    metaphor: 'Brakes on a software factory',
    thesis:
      'Agent speed without process brakes produces unreviewable slop. Split implementation from review, tier human attention by blast radius, and compound standards via retros.',
    hook:
      'Organizations already drowned in unreviewed PRs; AI multiplied the strain. Pocock frames skills as the rubric for faster, safer review.',
    durationMin: 23,
    transcriptWords: 4156,
    stats: [
      { value: '3', label: 'Quality layers: checks, agent review, human sign-off' },
      { value: '67K', label: 'Views on upload (public snapshot)', cite: 'TubeAlfred Oct 2026' },
      { value: '4.2K', label: 'Transcript words ingested (auto EN captions)' },
    ],
    symbols: [
      { term: 'Deep module', meaning: 'Simple public surface, complex interior — tests target behavior not brittle structure.' },
      { term: 'Review agent', meaning: 'Specialized sub-agent that fixes standards instead of only commenting.' },
      { term: 'Blast radius', meaning: 'One-way vs two-way doors — humans focus on irreversible change.' },
      { term: 'Retro skill', meaning: 'Mine past sessions to update coding standards and steering files.' },
    ],
    vocab: [
      { term: 'Slop', def: 'Low-quality PR volume that humans cannot parse at agent speed.', viz: 'review-gate' },
      { term: 'Skill', def: 'Reusable text artifact encoding team architecture and workflow.', viz: 'deep-module' },
      { term: 'Tautological test', def: 'Test that mirrors implementation — fragile under agent refactors.', viz: 'eval-loop' },
    ],
    failureModes: [
      { title: 'One agent does everything', body: 'Implementation + standards in one context overloads the model; review quality collapses.' },
      { title: 'Human-readable PR fiction', body: 'Summaries can hallucinate; code still must be read for high-risk merges.' },
      { title: 'Token theater', body: 'Multi-phase “make it work then good” without brakes burns budget and leaves slop.' },
    ],
    demoStages: [
      { label: 'Agent opens PR', meta: 'feature/auth-refactor' },
      { label: 'Deep-module tests', meta: 'interface-only' },
      { label: 'Review agent commits', meta: 'standards.md' },
      { label: 'Human tier-2 review', meta: 'two-way door' },
      { label: 'Retro updates skills', meta: 'compound' },
    ],
    diagram: 'pr-pipeline',
  },
  {
    slug: 'death-of-code-review',
    videoId: '_mi3alkqy4s',
    title: 'The Death of the Code Review',
    speaker: 'Laurie Voss',
    org: 'Arize AI',
    accent: '#fb7185',
    metaphor: 'Measurement replaces ritual',
    thesis:
      'Agent output velocity broke the social contract of code review. The replacement is eval discipline and observability — not bigger review queues.',
    hook:
      'Back-to-back with Pocock by design: same bottleneck, data-first framing from npm co-founder turned AI testing lead.',
    durationMin: 25,
    transcriptWords: 4412,
    stats: [
      { value: '↑', label: 'Agent code production vs flat human review bandwidth' },
      { value: '19K', label: 'Views on session upload' },
      { value: '4.4K', label: 'Words in auto-generated transcript' },
    ],
    symbols: [
      { term: 'Ritual review', meaning: 'LGTM culture that never scaled; now physically impossible.' },
      { term: 'Eval layer', meaning: 'Automated judgment on outputs before humans see noise.' },
      { term: 'Observability', meaning: 'Trace what agents changed and whether behavior regressed.' },
    ],
    vocab: [
      { term: 'Review cliff', def: 'Gap between merge rate and human comprehension rate.', viz: 'review-gate' },
      { term: 'Behavior test', def: 'Assert outcomes agents must preserve across edits.', viz: 'eval-loop' },
      { term: 'Signal', def: 'Metric that predicts incident cost better than line-count review.', viz: 'survey-radar' },
    ],
    failureModes: [
      { title: 'Scaling reviewers linearly', body: 'Headcount does not track token output; queue depth becomes permanent.' },
      { title: 'Rubber-stamp automation', body: 'Auto-approve without evals recreates the worst of pre-AI review culture.' },
      { title: 'Confusing demo for coverage', body: 'Happy-path tests miss agent-specific failure modes.' },
    ],
    demoStages: [
      { label: 'Agent flood', meta: '+40 PRs / week' },
      { label: 'Eval gate', meta: 'behavior suite' },
      { label: 'Drift detected', meta: 'trace diff' },
      { label: 'Human sample', meta: 'statistical' },
      { label: 'Ship', meta: 'with evidence' },
    ],
    diagram: 'review-cliff',
  },
  {
    slug: 'self-improving-factories',
    videoId: 'tUPPVhBBcoM',
    title: 'Self-Improving Software Factories',
    speaker: 'Zach Lloyd',
    org: 'Warp',
    accent: '#22d3ee',
    metaphor: 'Open-source factory floor',
    thesis:
      'Agentic dev environments become self-improving factories when the loop — code, test, reflect, patch — is productized and open source.',
    hook:
      'Former Google Docs principal engineer; claims six months shipping without hand-writing code, via Warp’s agentic terminal.',
    durationMin: 21,
    transcriptWords: 3636,
    stats: [
      { value: '6mo', label: 'No hand-written code (speaker claim, keynote)' },
      { value: '83K', label: 'Views — highest in Paris sample' },
      { value: 'OSS', label: 'Factory model pitched as open source' },
    ],
    symbols: [
      { term: 'Software factory', meaning: 'System that turns intents into merged code with minimal human typing.' },
      { term: 'Self-improve', meaning: 'Tooling updates its own prompts, skills, or scaffolds from outcomes.' },
      { term: 'Agentic IDE', meaning: 'Terminal-first environment where agents are first-class citizens.' },
    ],
    vocab: [
      { term: 'Loop', def: 'Closed cycle from spec to merge to retrospective.', viz: 'factory-line' },
      { term: 'Open weights / open tool', def: 'Factory stack you can inspect and fork.', viz: 'deep-module' },
      { term: 'Throughput', def: 'Merged outcomes per unit human attention.', viz: 'review-gate' },
    ],
    failureModes: [
      { title: 'Factory without brakes', body: 'Speed without Pocock-style review layers reintroduces slop at scale.' },
      { title: 'Closed black box', body: 'Proprietary factory → no community fixes to scaffolding.' },
      { title: 'Hero engineer dependency', body: 'Works for founders; enterprise needs standards and evals.' },
    ],
    demoStages: [
      { label: 'Intent', meta: 'issue #1842' },
      { label: 'Agent swarm', meta: 'warp agents' },
      { label: 'CI green', meta: '12 checks' },
      { label: 'Reflect', meta: 'skill patch' },
      { label: 'Merge', meta: 'main' },
    ],
    diagram: 'factory-loop',
  },
  {
    slug: 'build-a-factory',
    videoId: 'vGCJ7diEtrw',
    title: 'What It Actually Takes to Build a Software Factory',
    speaker: 'Tereza Tížková',
    org: 'Factory',
    accent: '#a78bfa',
    metaphor: 'Enterprise bill of materials',
    thesis:
      'Everyone says “factory”; few ship one. Definition, build-vs-buy, production references (EY, Adobe), and real cost dominate.',
    hook:
      'Factory.com builder separating hype from enterprise deployment requirements at Paris main stage.',
    durationMin: 23,
    transcriptWords: 3710,
    stats: [
      { value: '75K', label: 'Views on talk upload' },
      { value: '2', label: 'Named enterprise refs in opening (EY, Adobe)' },
      { value: '3.7K', label: 'Transcript words captured' },
    ],
    symbols: [
      { term: 'Definition', meaning: 'What counts as factory vs agent wrapper with a logo.' },
      { term: 'Build vs buy', meaning: 'Internal platform vs vendor-managed factory.' },
      { term: 'Cost model', meaning: 'Tokens, humans-in-loop, and change management — not just licenses.' },
    ],
    vocab: [
      { term: 'Production factory', def: 'Survives compliance, on-call, and legacy repos.', viz: 'enterprise-stack' },
      { term: 'Integration', def: 'SSO, audit logs, policy — not only codegen.', viz: 'deep-module' },
      { term: 'Change mgmt', def: 'Engineers must trust merged agent output.', viz: 'review-gate' },
    ],
    failureModes: [
      { title: 'Pilot forever', body: 'Demo on greenfield repo never touches monolith constraints.' },
      { title: 'Ignored economics', body: 'Token spend without productivity measurement burns budget.' },
      { title: 'Vendor lock-in', body: 'Factory you cannot export or audit fails regulated customers.' },
    ],
    demoStages: [
      { label: 'Assess', meta: 'legacy + policy' },
      { label: 'Choose', meta: 'build / buy' },
      { label: 'Integrate', meta: 'SSO + audit' },
      { label: 'Pilot', meta: 'one domain' },
      { label: 'Scale', meta: 'cost model' },
    ],
    diagram: 'build-buy',
  },
  {
    slug: 'orchestras-not-factories',
    videoId: 'TRfzFJCJ7ZE',
    title: 'Orchestras, Not Factories',
    speaker: 'Charlie Holtz',
    org: 'Conductor',
    accent: '#fbbf24',
    metaphor: 'Conductor’s baton',
    thesis:
      'Fast builders run parallel coding agents like sections in an orchestra — coordination and score matter more than a single assembly line.',
    hook:
      'Conductor desktop app for managing many agents; counter-narrative to factory monoculture on the same Paris floor.',
    durationMin: 18,
    transcriptWords: 3083,
    stats: [
      { value: '31K', label: 'Views on upload' },
      { value: 'N', label: 'Parallel agent lanes (product metaphor)' },
      { value: '3.1K', label: 'Transcript words' },
    ],
    symbols: [
      { term: 'Conductor', meaning: 'Human (or UI) coordinating simultaneous agent workstreams.' },
      { term: 'Section', meaning: 'Agent with a part — frontend, tests, docs — not one mega-prompt.' },
      { term: 'Score', meaning: 'Shared plan / spec agents follow in time.' },
    ],
    vocab: [
      { term: 'Parallelism', def: 'Many agents, synchronized checkpoints.', viz: 'orchestra' },
      { term: 'Factory critique', def: 'Assembly line hides coordination failures until merge.', viz: 'factory-line' },
      { term: 'Desktop control', def: 'Local app for visibility into agent state.', viz: 'deep-module' },
    ],
    failureModes: [
      { title: 'Orchestra without score', body: 'Parallel agents diverge; integration cost explodes at merge.' },
      { title: 'Conductor bottleneck', body: 'One human cannot baton every lane at enterprise scale.' },
      { title: 'Factory envy', body: 'Copying vendor narrative without your team’s coordination culture.' },
    ],
    demoStages: [
      { label: 'Score loaded', meta: 'spec.md' },
      { label: 'Strings', meta: 'UI agent' },
      { label: 'Brass', meta: 'test agent' },
      { label: 'Percussion', meta: 'deploy agent' },
      { label: 'Crescendo', meta: 'merge' },
    ],
    diagram: 'orchestra-pit',
  },
  {
    slug: 'state-of-ai-dev',
    videoId: 'Se8jHLliLXE',
    title: 'The State of AI in Software Development',
    speaker: 'Justin Reock',
    org: 'DX',
    accent: '#34d399',
    metaphor: 'Instrument panel',
    thesis:
      'Quarterly DX research across 400+ organizations grounds AI hype in developer experience and productivity metrics — DORA/SPACE lineage.',
    hook:
      'Deputy CTO DX; platform built by folks behind DORA metrics and DevX framework — data not keynote adjectives.',
    durationMin: 19,
    transcriptWords: 3787,
    stats: [
      { value: '400+', label: 'Organizations in DX research sample (speaker)' },
      { value: '11K', label: 'Views on upload' },
      { value: '3.8K', label: 'Transcript words ingested' },
    ],
    symbols: [
      { term: 'DevEx', meaning: 'How engineers experience tooling change — not just output lines.' },
      { term: 'Quarterly report', meaning: 'Recurring measurement beats one-off surveys.' },
      { term: 'Platform signal', meaning: 'Aggregated trends vs anecdotal Twitter threads.' },
    ],
    vocab: [
      { term: 'Adoption', def: 'Who uses AI tools vs who benefits.', viz: 'survey-radar' },
      { term: 'Productivity', def: 'Outcome metrics, not vanity commit counts.', viz: 'eval-loop' },
      { term: 'Friction', def: 'Where AI slows experts down.', viz: 'review-gate' },
    ],
    failureModes: [
      { title: 'Metric shopping', body: 'Cherry-pick one KPI that proves AI success.' },
      { title: 'Ignore DevEx', body: 'Throughput up while satisfaction and quality collapse.' },
      { title: 'Static snapshot', body: 'One survey year — models and tools move quarterly.' },
    ],
    demoStages: [
      { label: 'Ingest', meta: '400 orgs' },
      { label: 'Normalize', meta: 'DORA lineage' },
      { label: 'Trend', meta: 'QoQ AI impact' },
      { label: 'Segment', meta: 'role × size' },
      { label: 'Report', meta: 'state of AI' },
    ],
    diagram: 'dx-radar',
  },
]

export function getTalk(slug: string): Talk | undefined {
  return talks.find((t) => t.slug === slug)
}
