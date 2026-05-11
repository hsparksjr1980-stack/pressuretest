export default function ArticlePage() {
  return (
    <main className="min-h-screen bg-[#0b0f14] px-6 py-20 text-white">
      <article className="mx-auto max-w-4xl">
        <a
          href="/blog"
          className="text-sm text-slate-500 hover:text-white"
        >
          ← Back to Blog
        </a>

        <p className="mt-16 mb-4 text-sm uppercase tracking-[0.3em] text-slate-500">
          Operations
        </p>

        <h1 className="text-5xl font-bold leading-tight md:text-6xl">
          What First-Time Franchise Buyers Underestimate
        </h1>

        <p className="mt-8 text-lg leading-8 text-slate-300">
          Many first-time operators spend most of their diligence process focused
          on startup cost estimates, brand reputation, and projected revenue.
          Far fewer spend enough time reviewing operational pressure.
        </p>

        <div className="mt-14 space-y-10 leading-8 text-slate-300">
          <section>
            <h2 className="mb-4 text-3xl font-semibold">
              Staffing Is Usually Harder Than Expected
            </h2>

            <p>
              Many operating models assume labor availability, smooth hiring,
              reliable shift coverage, and stable employee retention. In reality,
              staffing pressure often becomes one of the largest operational
              risks during the first year.
            </p>
          </section>

          <section>
            <h2 className="mb-4 text-3xl font-semibold">
              Ramp Timing Often Slows Down
            </h2>

            <p>
              New operators frequently underestimate how long it takes for
              customer acquisition, local awareness, staffing stability, and
              operational efficiency to stabilize after launch.
            </p>
          </section>

          <section>
            <h2 className="mb-4 text-3xl font-semibold">
              Working Capital Pressure Builds Quietly
            </h2>

            <p>
              Startup budgets may account for opening costs without fully
              accounting for slower ramp periods, labor inefficiency, inventory
              mistakes, marketing variability, or owner draw requirements.
            </p>
          </section>

          <section>
            <h2 className="mb-4 text-3xl font-semibold">
              Operational Complexity Compounds
            </h2>

            <p>
              Vendor coordination, scheduling, compliance requirements,
              equipment downtime, staffing coverage, local competition, and
              customer expectations create layers of operational pressure that
              are difficult to appreciate before launch.
            </p>
          </section>

          <section>
            <h2 className="mb-4 text-3xl font-semibold">
              Diligence Should Extend Beyond Optimistic Assumptions
            </h2>

            <p>
              Strong diligence is not about predicting failure. It is about
              identifying pressure points early enough to prepare realistically
              before committing significant capital.
            </p>
          </section>
        </div>
      </article>
    </main>
  );
}