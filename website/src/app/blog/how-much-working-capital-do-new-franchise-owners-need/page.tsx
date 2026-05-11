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
          Cash Flow
        </p>

        <h1 className="text-5xl font-bold leading-tight md:text-6xl">
          How Much Working Capital Do New Franchise Owners Actually Need?
        </h1>

        <p className="mt-8 text-lg leading-8 text-slate-300">
          Many operators focus heavily on franchise fees and buildout costs
          while underestimating the amount of liquidity required after opening.
        </p>

        <div className="mt-14 space-y-10 leading-8 text-slate-300">
          <section>
            <h2 className="mb-4 text-3xl font-semibold">
              Startup Costs Are Only Part Of The Equation
            </h2>

            <p>
              Opening budgets often focus on construction, equipment, inventory,
              and franchise fees. But the operating period after launch is where
              cash pressure frequently intensifies.
            </p>
          </section>

          <section>
            <h2 className="mb-4 text-3xl font-semibold">
              Revenue Usually Takes Time To Stabilize
            </h2>

            <p>
              Early sales volatility can create pressure when payroll, rent,
              utilities, loan payments, and vendor obligations continue
              regardless of customer ramp speed.
            </p>
          </section>

          <section>
            <h2 className="mb-4 text-3xl font-semibold">
              Labor Inefficiency Can Drain Cash
            </h2>

            <p>
              New teams are rarely fully optimized at launch. Overtime,
              turnover, scheduling inefficiency, and training costs can create
              unexpected operating strain.
            </p>
          </section>

          <section>
            <h2 className="mb-4 text-3xl font-semibold">
              Operators Often Underestimate Time Pressure
            </h2>

            <p>
              Owners may need additional reserves if they cannot immediately
              replace prior income or if operational demands reduce outside
              earning flexibility.
            </p>
          </section>

          <section>
            <h2 className="mb-4 text-3xl font-semibold">
              Conservative Planning Improves Flexibility
            </h2>

            <p>
              Strong diligence includes modeling slower ramps, higher expenses,
              and larger reserve cushions than optimistic scenarios assume.
            </p>
          </section>
        </div>
      </article>
    </main>
  );
}