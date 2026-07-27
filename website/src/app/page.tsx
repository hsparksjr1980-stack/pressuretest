import Link from "next/link";

const focusAreas = [
  {
    title: "Operator fit",
    body: "Clarify whether the opportunity matches your time, capital, risk tolerance, and operating reality.",
  },
  {
    title: "Working capital pressure",
    body: "Review how much cash strain could appear before the location reaches steady-state operations.",
  },
  {
    title: "Ramp timing",
    body: "Separate hopeful launch assumptions from the slower, messier ramp scenarios worth planning for.",
  },
  {
    title: "Staffing assumptions",
    body: "Look at hiring, management coverage, training load, and owner involvement before they become surprises.",
  },
  {
    title: "Buildout risk",
    body: "Surface lease, construction, equipment, permitting, and opening-cost questions while there is still time.",
  },
  {
    title: "Execution readiness",
    body: "Turn open diligence questions into a clearer go, pause, or revisit decision path.",
  },
];

const workflowSteps = [
  "Start Here",
  "Operator Fit",
  "Opportunity Review",
  "Financial Reality",
  "Commitment Review",
  "Final Decision",
  "Report",
];

const reviewItems = [
  ["Capital cushion", "Needs review", "amber"],
  ["Owner time load", "High pressure", "red"],
  ["Territory confidence", "Documented", "green"],
  ["Ramp assumptions", "Stress test", "amber"],
];

export default function Home() {
  return (
    <main className="site-shell min-h-screen text-white">
      <section className="overflow-hidden px-6 py-16 md:py-24">
        <div className="mx-auto grid max-w-6xl items-center gap-14 lg:grid-cols-[1.05fr_0.95fr]">
          <div>
            <p className="mb-5 text-sm font-semibold uppercase tracking-[0.24em] text-red-300">
              PressureTest: Franchise
            </p>

            <h1 className="max-w-5xl text-5xl font-bold leading-[1.04] md:text-7xl">
              Pressure test the business before the business pressure tests you.
            </h1>

            <p className="mt-8 max-w-3xl text-lg leading-8 text-slate-300">
              PressureTest helps prospective franchise operators organize
              diligence, review assumptions, identify operational pressure
              points, and prepare for ownership decisions before signing,
              borrowing, leasing, or investing.
            </p>

            <div className="mt-10 flex flex-wrap gap-4">
              <Link
                href="/how-it-works"
                className="rounded-lg bg-white px-6 py-3 font-semibold text-black transition hover:bg-slate-200"
              >
                See How It Works
              </Link>

              <Link
                href="/contact"
                className="rounded-lg border border-slate-600 px-6 py-3 font-semibold text-white transition hover:border-red-300"
              >
                Join Waitlist
              </Link>
            </div>

            <div className="mt-12 grid max-w-2xl gap-5 border-t border-white/10 pt-8 text-sm text-slate-400 sm:grid-cols-3">
              <div>
                <p className="text-2xl font-semibold text-white">7</p>
                <p className="mt-1">Franchise Beta workflow steps</p>
              </div>
              <div>
                <p className="text-2xl font-semibold text-white">4</p>
                <p className="mt-1">Decision zones reviewed</p>
              </div>
              <div>
                <p className="text-2xl font-semibold text-white">1</p>
                <p className="mt-1">Structured report to revisit</p>
              </div>
            </div>
          </div>

          <div className="glass-panel glass-highlight rounded-lg p-5">
            <div className="glass-panel-soft mb-6 flex items-center justify-between rounded-md p-4">
              <div className="flex items-center gap-3">
                <span
                  aria-hidden="true"
                  className="glass-panel-soft relative grid h-12 w-12 place-items-center rounded-full"
                >
                  <span className="absolute h-8 w-8 rounded-full border-[6px] border-slate-700 border-r-red-500 border-t-amber-300" />
                  <span className="absolute h-1 w-5 origin-left rotate-[-38deg] rounded-full bg-red-400" />
                  <span className="relative h-3 w-3 rounded-full bg-white" />
                </span>
                <div>
                  <p className="text-xl font-black italic text-slate-100">
                    Pressure<span className="text-red-500">Test</span>
                  </p>
                  <p className="mt-1 text-xs font-semibold uppercase tracking-[0.18em] text-slate-500">
                    Franchise diligence workspace
                  </p>
                </div>
              </div>
              <span className="hidden rounded-md bg-red-500/15 px-3 py-1 text-sm font-semibold text-red-200 sm:inline">
                Beta
              </span>
            </div>

            <div className="glass-panel-soft rounded-lg p-5">
              <div className="flex items-center justify-between border-b border-white/10 pb-4">
                <div>
                  <p className="text-xs font-semibold uppercase tracking-[0.2em] text-slate-500">
                    Live Review
                  </p>
                  <h2 className="mt-2 text-xl font-semibold">
                    Franchise pressure map
                  </h2>
                </div>
                <span className="rounded-md bg-red-500/15 px-3 py-1 text-sm font-semibold text-red-200">
                  Beta
                </span>
              </div>

              <div className="mt-5 space-y-3">
                {reviewItems.map(([label, status, tone]) => (
                  <div
                    key={label}
                    className="grid grid-cols-[1fr_auto] items-center gap-4 rounded-md border border-white/10 bg-white/5 p-4"
                  >
                    <span className="text-sm text-slate-300">{label}</span>
                    <span
                      className={[
                        "rounded-md px-3 py-1 text-xs font-semibold",
                        tone === "green"
                          ? "bg-emerald-500/15 text-emerald-200"
                          : tone === "red"
                            ? "bg-red-500/15 text-red-200"
                            : "bg-amber-400/15 text-amber-200",
                      ].join(" ")}
                    >
                      {status}
                    </span>
                  </div>
                ))}
              </div>
            </div>

            <div className="mt-6 grid gap-3 sm:grid-cols-3">
              {["Fit", "Cash", "Ramp"].map((item, index) => (
                <div
                  key={item}
                  className="glass-panel-soft rounded-md p-4"
                >
                  <p className="text-xs font-semibold uppercase tracking-[0.18em] text-slate-500">
                    {item}
                  </p>
                  <div className="mt-4 h-2 rounded-full bg-slate-800">
                    <div
                      className={[
                        "h-2 rounded-full",
                        index === 0
                          ? "w-2/3 bg-emerald-400"
                          : index === 1
                            ? "w-1/2 bg-amber-300"
                            : "w-4/5 bg-red-400",
                      ].join(" ")}
                    />
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      <section className="border-y border-white/10 bg-white/[0.045] px-6 py-14 backdrop-blur-xl">
        <div className="mx-auto grid max-w-6xl gap-5 md:grid-cols-7">
          {workflowSteps.map((step, index) => (
            <div key={step} className="min-h-28 border-l border-white/15 pl-4">
              <p className="text-sm font-semibold text-red-300">
                {String(index + 1).padStart(2, "0")}
              </p>
              <p className="mt-4 text-sm font-semibold leading-5 text-white">
                {step}
              </p>
            </div>
          ))}
        </div>
      </section>

      <section className="px-6 py-24">
        <div className="mx-auto max-w-6xl">
          <p className="mb-5 text-sm font-semibold uppercase tracking-[0.24em] text-slate-500">
            What Gets Tested
          </p>
          <h2 className="max-w-3xl text-3xl font-bold leading-tight md:text-5xl">
            Built for the diligence questions that usually get answered too
            late.
          </h2>

          <div className="mt-10 grid gap-4 md:grid-cols-3">
            {focusAreas.map((item) => (
              <div
                key={item.title}
                className="glass-panel-soft rounded-lg p-6"
              >
                <h3 className="text-lg font-semibold text-white">
                  {item.title}
                </h3>
                <p className="mt-3 text-sm leading-6 text-slate-400">
                  {item.body}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className="border-y border-white/10 bg-white/[0.82] px-6 py-24 text-slate-950 backdrop-blur-xl">
        <div className="mx-auto grid max-w-6xl gap-12 md:grid-cols-[0.9fr_1.1fr]">
          <div>
            <p className="mb-5 text-sm font-semibold uppercase tracking-[0.24em] text-red-700">
              Positioning
            </p>
            <h2 className="text-3xl font-bold leading-tight md:text-5xl">
              Not a broker. Not an advisor. Not a hype machine.
            </h2>
          </div>

          <div className="space-y-6 text-lg leading-8 text-slate-700">
            <p>
              PressureTest is educational diligence software for prospective
              operators who want a calmer way to examine a franchise opportunity
              before serious commitments begin stacking up.
            </p>
            <p>
              The product is built to slow the process down, capture unresolved
              questions, and make assumptions easier to revisit with appropriate
              professional support.
            </p>
          </div>
        </div>
      </section>

      <section className="px-6 py-20">
        <div className="mx-auto flex max-w-6xl flex-col items-start justify-between gap-8 border-t border-white/10 pt-12 md:flex-row md:items-center">
          <div>
            <p className="text-sm font-semibold uppercase tracking-[0.24em] text-slate-500">
              Next Step
            </p>
            <h2 className="mt-4 max-w-3xl text-3xl font-bold leading-tight md:text-5xl">
              Bring structure to the questions you cannot afford to hand-wave.
            </h2>
          </div>

          <Link
            href="/contact"
            className="rounded-lg bg-white px-6 py-3 font-semibold text-black transition hover:bg-slate-200"
          >
            Join Waitlist
          </Link>
        </div>
      </section>
    </main>
  );
}
