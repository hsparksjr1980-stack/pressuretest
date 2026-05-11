export default function DataUsePage() {
  return (
    <main className="min-h-screen bg-[#0b0f14] px-6 py-20 text-white">
      <section className="mx-auto max-w-4xl">
        <p className="mb-4 text-sm uppercase tracking-[0.3em] text-slate-500">
          Data Use
        </p>

        <h1 className="text-5xl font-bold leading-tight md:text-6xl">
          How PressureTest Uses Data
        </h1>

        <p className="mt-6 text-slate-400">Last updated: May 11, 2026</p>

        <div className="mt-12 space-y-10 leading-8 text-slate-300">
          <section>
            <h2 className="mb-3 text-2xl font-semibold text-white">
              Purpose of Data Use
            </h2>
            <p>
              PressureTest uses user-provided information to help structure
              diligence workflows, generate educational outputs, organize
              assumptions, and identify operational pressure points.
            </p>
          </section>

          <section>
            <h2 className="mb-3 text-2xl font-semibold text-white">
              User-Provided Inputs
            </h2>
            <p>
              Users may enter assumptions related to startup costs, working
              capital, staffing, ramp timing, revenue expectations, operating
              risks, and business readiness. These inputs are used to generate
              educational diligence summaries and planning outputs.
            </p>
          </section>

          <section>
            <h2 className="mb-3 text-2xl font-semibold text-white">
              No Outcome Guarantees
            </h2>
            <p>
              PressureTest does not predict success or failure, recommend
              investments, endorse franchise systems, or validate the accuracy
              of user assumptions. Outputs are educational and should be
              independently verified.
            </p>
          </section>

          <section>
            <h2 className="mb-3 text-2xl font-semibold text-white">
              Data Accuracy
            </h2>
            <p>
              The quality of PressureTest outputs depends on the quality and
              completeness of information provided by the user. Users are
              responsible for validating assumptions with qualified
              professionals and independent sources.
            </p>
          </section>

          <section>
            <h2 className="mb-3 text-2xl font-semibold text-white">
              Future Product Development
            </h2>
            <p>
              Aggregated or non-identifying usage patterns may be reviewed to
              improve workflows, content, calculators, reports, and platform
              usability.
            </p>
          </section>

          <p className="text-sm text-slate-500">
            This page is a working draft and should be reviewed by qualified
            counsel before public launch.
          </p>
        </div>
      </section>
    </main>
  );
}