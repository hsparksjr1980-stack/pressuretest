export default function Home() {
  return (
    <main className="min-h-screen bg-[#0b0f14] px-6 py-8 text-white">
      <section className="mx-auto max-w-6xl py-24">
        <p className="mb-5 text-sm uppercase tracking-[0.3em] text-slate-400">
          Franchise & Small-Business Diligence
        </p>

        <h1 className="max-w-4xl text-5xl font-bold leading-tight tracking-tight md:text-7xl">
          Pressure test the business before the business pressure tests you.
        </h1>

        <p className="mt-8 max-w-2xl text-lg leading-8 text-slate-300">
          PressureTest helps prospective operators review assumptions, cash
          pressure, ramp timing, staffing realities, and operational risk before
          committing capital.
        </p>

        <div className="mt-10 flex flex-wrap gap-4">
          <a
            href="#"
            className="rounded-xl bg-white px-6 py-3 font-semibold text-black hover:bg-slate-200"
          >
            Run a Pressure Test
          </a>

          <a
            href="how-it-works"
            className="rounded-xl border border-slate-700 px-6 py-3 font-semibold text-white hover:border-slate-500"
          >
            See How It Works
          </a>
        </div>
      </section>

      <section id="evaluates" className="mx-auto max-w-6xl py-16">
        <div className="mb-10 max-w-2xl">
          <p className="mb-3 text-sm uppercase tracking-[0.25em] text-slate-500">
            What It Evaluates
          </p>

          <h2 className="text-3xl font-bold md:text-4xl">
            Built around the pressure points that actually matter.
          </h2>
        </div>

        <div className="grid gap-6 md:grid-cols-3">
          <div className="rounded-2xl border border-slate-800 bg-slate-950 p-6">
            <h3 className="mb-3 text-xl font-semibold">Reality Check</h3>
            <p className="leading-7 text-slate-400">
              Review operator fit, personal risk tolerance, time demands, and
              whether the opportunity matches the reality of ownership.
            </p>
          </div>

          <div className="rounded-2xl border border-slate-800 bg-slate-950 p-6">
            <h3 className="mb-3 text-xl font-semibold">Financial Stress Test</h3>
            <p className="leading-7 text-slate-400">
              Pressure test cash needs, ramp timing, labor assumptions, working
              capital, downside scenarios, and break-even pressure.
            </p>
          </div>

          <div className="rounded-2xl border border-slate-800 bg-slate-950 p-6">
            <h3 className="mb-3 text-xl font-semibold">Operational Risk</h3>
            <p className="leading-7 text-slate-400">
              Identify staffing complexity, buildout risk, vendor dependency,
              local market pressure, and execution constraints.
            </p>
          </div>
        </div>
      </section>

      <section id="how-it-works" className="mx-auto max-w-6xl py-20">
        <div className="mb-10 max-w-2xl">
          <p className="mb-3 text-sm uppercase tracking-[0.25em] text-slate-500">
            How It Works
          </p>

          <h2 className="text-3xl font-bold md:text-4xl">
            A structured diligence workflow, not a sales pitch.
          </h2>
        </div>

        <div className="grid gap-4">
          {[
            ["01", "Reality Check", "Clarify fit, constraints, risk tolerance, and operating expectations."],
            ["02", "Assumption Review", "Document the assumptions behind revenue, labor, ramp speed, expenses, and market demand."],
            ["03", "Financial Pressure Test", "Model what happens if sales ramp slower, costs run higher, or cash reserves get tight."],
            ["04", "Decision Readiness", "Summarize open questions, pressure points, and what needs validation before moving forward."],
          ].map(([number, title, body]) => (
            <div
              key={title}
              className="grid gap-4 rounded-2xl border border-slate-800 bg-slate-950 p-6 md:grid-cols-[80px_1fr]"
            >
              <div className="text-sm font-semibold text-slate-500">{number}</div>
              <div>
                <h3 className="mb-2 text-xl font-semibold">{title}</h3>
                <p className="leading-7 text-slate-400">{body}</p>
              </div>
            </div>
          ))}
        </div>
      </section>

      <section className="mx-auto max-w-6xl py-20">
        <div className="rounded-3xl border border-slate-800 bg-slate-950 p-8 md:p-12">
          <h2 className="max-w-3xl text-3xl font-bold md:text-5xl">
            The goal is not to predict success. The goal is to find pressure
            before it finds you.
          </h2>

          <p className="mt-6 max-w-2xl leading-8 text-slate-400">
            PressureTest is designed for prospective operators who want a more
            disciplined way to evaluate business opportunities before signing,
            financing, leasing, hiring, or committing serious capital.
          </p>

          <div className="mt-8">
            <a
              href="#"
              className="rounded-xl bg-white px-6 py-3 font-semibold text-black hover:bg-slate-200"
            >
              Start Pressure Testing
            </a>
          </div>
        </div>
      </section>

      <section id="disclaimer" className="mx-auto max-w-6xl border-t border-slate-800 py-10">
        <p className="max-w-4xl text-sm leading-6 text-slate-500">
          PressureTest is an educational diligence and operational planning tool.
          It does not provide legal, tax, accounting, lending, financial, or
          investment advice. Users should independently validate assumptions and
          consult qualified professionals before making business decisions.
        </p>
      </section>
    </main>
  );
}