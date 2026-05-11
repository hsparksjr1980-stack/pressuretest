const tiers = [
  {
    name: "Free",
    price: "$0",
    description: "For early exploration and basic diligence structure.",
    features: [
      "Basic opportunity review",
      "Initial risk prompts",
      "Educational diligence framework",
      "No saved reports yet",
    ],
  },
  {
    name: "Starter",
    price: "TBD",
    description: "For buyers actively comparing a real opportunity.",
    features: [
      "Full pressure test workflow",
      "Assumption review",
      "Financial stress-test guidance",
      "Downloadable summary report",
    ],
  },
  {
    name: "Operator",
    price: "TBD",
    description: "For serious buyers preparing for execution.",
    features: [
      "Expanded operational review",
      "Cash pressure planning",
      "Staffing and ramp-risk review",
      "Decision-readiness summary",
    ],
  },
];

export default function Pricing() {
  return (
    <main className="min-h-screen bg-[#0b0f14] px-6 py-20 text-white">
      <section className="mx-auto max-w-6xl">
        <p className="mb-4 text-sm uppercase tracking-[0.3em] text-slate-500">
          Pricing
        </p>

        <h1 className="max-w-4xl text-5xl font-bold leading-tight md:text-7xl">
          Start with structure. Pay later when the workflow is worth it.
        </h1>

        <p className="mt-8 max-w-2xl text-lg leading-8 text-slate-300">
          Pricing is intentionally placeholder while PressureTest validates
          what prospective operators actually need before committing capital.
        </p>

        <div className="mt-16 grid gap-6 md:grid-cols-3">
          {tiers.map((tier) => (
            <div
              key={tier.name}
              className="rounded-2xl border border-slate-800 bg-slate-950 p-6"
            >
              <h2 className="text-2xl font-semibold">{tier.name}</h2>
              <p className="mt-4 text-4xl font-bold">{tier.price}</p>
              <p className="mt-4 leading-7 text-slate-400">
                {tier.description}
              </p>

              <ul className="mt-6 space-y-3 text-sm text-slate-300">
                {tier.features.map((feature) => (
                  <li key={feature}>• {feature}</li>
                ))}
              </ul>

              <a
                href="/contact"
                className="mt-8 inline-block rounded-xl bg-white px-5 py-3 font-semibold text-black hover:bg-slate-200"
              >
                Join Waitlist
              </a>
            </div>
          ))}
        </div>
      </section>
    </main>
  );
}