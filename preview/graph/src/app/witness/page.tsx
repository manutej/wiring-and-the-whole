export default function WitnessPage() {
  return (
    <article className="space-y-4">
      <div>
        <h2 className="text-xl font-normal mb-2">E1 faithfulness witness</h2>
        <p className="text-sm text-[var(--mute)] font-sans max-w-2xl">
          Static instrument from{" "}
          <code className="font-mono text-xs">docs/witness/index.html</code>{" "}
          (copied to{" "}
          <code className="font-mono text-xs">public/witness/</code> for this
          deploy).
        </p>
      </div>
      <iframe
        title="E1 witness instrument"
        src="/witness/index.html"
        className="witness-frame"
      />
    </article>
  );
}
