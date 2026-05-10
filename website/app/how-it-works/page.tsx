export default function HowItWorks() {
  return (
    <main className="min-h-screen bg-[#0b0f14] px-6 py-8 text-white">
      <section className="mx-auto max-w-6xl py-20">
        <a href="/" className="text-sm text-slate-400 hover:text-white">
          ← Back to Home
        </a>

        <p className="mt-16 mb-4 text-sm uppercase tracking-[0.3em] text-slate-500">
          How It Works
        </p>

        <h1 className="max-w-4xl text-5xl font-bold leading-tight md:text-7xl">
          A structured way to slow down before you sign.
        </h1>

        <p className="mt-8 max-w-2xl text-lg leading-8 text-slate-300">
          PressureTest helps organize diligence into a practical review process:
          fit, assumptions, financial pressure, and decision readiness.
        </p>

        <div className="mt-16 grid gap-6">
          {[
            [
              "01",
              "Reality Check",
              "Clarify whether the opportunity fits your time, capital, risk tolerance, family constraints, and operating expectations.",
            ],
            [
              "02",
              "Assumption Review",
              "Document the assumptions behind sales, labor, ramp speed, expenses, vendor support, territory, and market demand.",
            ],
            [
              "03",
              "Financial Stress Test",
              "Review what happens if costs run high, revenue ramps slowly, working capital gets tight, or staffing is harder than expected.",
            ],
            [
              "04",
              "Decision Readiness",
              "Summarize pressure points, unresolved questions, validation gaps, and what must be reviewed before moving forward.",
            ],
          ].map(([number, title, body]) => (
            <div
              key={title}
              className="grid gap-4 rounded-2xl border border-slate-800 bg-slate-950 p-6 md:grid-cols-[80px_1fr]"
            >
              <div className="text-sm font-semibold text-slate-500">
                {number}
              </div>

              <div>
                <h2 className="mb-2 text-2xl font-semibold">{title}</h2>
                <p className="leading-7 text-slate-400">{body}</p>
              </div>
            </div>
          ))}
        </div>
      </section>
    </main>
  );
}