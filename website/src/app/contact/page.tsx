import Link from "next/link";

const reviewAreas = [
  "Franchise diligence workflows",
  "Startup readiness workflows",
  "Financial pressure testing",
  "Decision-readiness reporting",
];

export default function Contact() {
  return (
    <main className="min-h-screen bg-[#0b0f14] px-6 py-20 text-white">
      <section className="mx-auto grid max-w-6xl gap-12 lg:grid-cols-[1fr_420px]">
        <div>
          <p className="mb-5 text-sm uppercase tracking-[0.3em] text-slate-500">
            Waitlist
          </p>

          <h1 className="max-w-4xl text-5xl font-bold leading-tight md:text-7xl">
            Early access for operators who want to pressure test before they
            commit.
          </h1>

          <p className="mt-8 max-w-2xl text-lg leading-8 text-slate-300">
            PressureTest is being shaped around real diligence moments:
            comparing opportunities, challenging assumptions, and deciding what
            still needs proof before capital is at risk.
          </p>

          <div className="mt-10 flex flex-wrap gap-4">
            <Link
              href="/pricing"
              className="rounded-xl bg-white px-6 py-3 font-semibold text-black hover:bg-slate-200"
            >
              View Pricing
            </Link>

            <Link
              href="/how-it-works"
              className="rounded-xl border border-slate-700 px-6 py-3 font-semibold text-white hover:border-slate-500"
            >
              See How It Works
            </Link>
          </div>
        </div>

        <aside className="self-start rounded-lg border border-slate-800 bg-slate-950 p-6">
          <h2 className="text-2xl font-semibold">What early users review</h2>

          <div className="mt-6 space-y-4 text-slate-300">
            {reviewAreas.map((area) => (
              <div key={area} className="border-b border-slate-800 pb-4">
                {area}
              </div>
            ))}
          </div>

          <p className="mt-6 text-sm leading-6 text-slate-500">
            The public waitlist intake is not connected yet. This page keeps the
            navigation path ready while the product workflow is finalized.
          </p>
        </aside>
      </section>
    </main>
  );
}
