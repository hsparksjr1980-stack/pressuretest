export default function ArticlePage() {
  return (
    <main className="min-h-screen bg-[#0b0f14] px-6 py-20 text-white">
      <article className="mx-auto max-w-4xl">
        <a href="/blog" className="text-sm text-slate-500 hover:text-white">
          ← Back to Blog
        </a>

        <p className="mt-16 mb-4 text-sm uppercase tracking-[0.3em] text-slate-500">
          Diligence
        </p>

        <h1 className="text-5xl font-bold leading-tight md:text-6xl">
          Pressure Testing Revenue Assumptions Before Signing
        </h1>

        <p className="mt-8 text-lg leading-8 text-slate-300">
          Revenue projections can look reasonable until the assumptions behind
          them are slowed down and reviewed under less favorable conditions.
        </p>

        <div className="mt-14 space-y-10 leading-8 text-slate-300">
          <section>
            <h2 className="mb-4 text-3xl font-semibold">
              Start With The Source
            </h2>
            <p>
              Revenue assumptions should be traced back to their source. A
              franchisor estimate, broker comment, peer operator example, or
              optimistic spreadsheet may each carry different reliability.
            </p>
          </section>

          <section>
            <h2 className="mb-4 text-3xl font-semibold">
              Review Ramp Speed Separately
            </h2>
            <p>
              A revenue target is incomplete without a ramp timeline. Operators
              should review what happens if sales take longer to stabilize than
              expected.
            </p>
          </section>

          <section>
            <h2 className="mb-4 text-3xl font-semibold">
              Separate Demand From Execution
            </h2>
            <p>
              Even if local demand exists, execution constraints such as
              staffing, location quality, marketing consistency, and service
              reliability may affect actual performance.
            </p>
          </section>

          <section>
            <h2 className="mb-4 text-3xl font-semibold">
              Model Less Favorable Scenarios
            </h2>
            <p>
              Pressure testing means asking what happens if revenue is lower,
              expenses are higher, ramp is slower, or cash reserves are thinner
              than planned.
            </p>
          </section>

          <section>
            <h2 className="mb-4 text-3xl font-semibold">
              The Goal Is Better Preparation
            </h2>
            <p>
              The purpose is not to reject every opportunity. The purpose is to
              understand which assumptions need validation before the operator
              signs, borrows, leases, hires, or commits capital.
            </p>
          </section>
        </div>
      </article>
    </main>
  );
}