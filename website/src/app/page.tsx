const focusAreas = [
  "Operator fit",
  "Working capital pressure",
  "Ramp timing",
  "Staffing assumptions",
  "Buildout risk",
  "Execution readiness",
];

export default function Home() {
  return (
    <main className="min-h-screen bg-[#0b0f14] px-6 py-20 text-white">
      <section className="mx-auto max-w-6xl">
        <p className="mb-5 text-sm uppercase tracking-[0.3em] text-slate-500">
          Franchise & Small-Business Diligence
        </p>

        <h1 className="max-w-5xl text-5xl font-bold leading-tight tracking-tight md:text-7xl">
          Pressure test the business before the business pressure tests you.
        </h1>

        <p className="mt-8 max-w-3xl text-lg leading-8 text-slate-300">
          PressureTest helps prospective operators organize diligence, review
          assumptions, identify operational pressure points, and prepare for the
          realities of ownership before committing serious capital.
        </p>

        <div className="mt-10 flex flex-wrap gap-4">
          <a
            href="/how-it-works"
            className="rounded-xl bg-white px-6 py-3 font-semibold text-black hover:bg-slate-200"
          >
            See How It Works
          </a>

          <a
            href="/pricing"
            className="rounded-xl border border-slate-700 px-6 py-3 font-semibold text-white hover:border-slate-500"
          >
            View Pricing
          </a>
        </div>
      </section>

      <section className="mx-auto mt-24 max-w-6xl border-t border-slate-800 pt-16">
        <h2 className="max-w-3xl text-3xl font-bold md:text-4xl">
          Built for the diligence questions that usually get answered too late.
        </h2>

        <div className="mt-10 grid gap-4 md:grid-cols-3">
          {focusAreas.map((item) => (
            <div
              key={item}
              className="rounded-2xl border border-slate-800 bg-slate-950 p-6 text-slate-300"
            >
              {item}
            </div>
          ))}
        </div>
      </section>

      <section className="mx-auto mt-24 max-w-6xl">
        <div className="rounded-3xl border border-slate-800 bg-slate-950 p-8 md:p-12">
          <p className="mb-4 text-sm uppercase tracking-[0.3em] text-slate-500">
            Positioning
          </p>

          <h2 className="max-w-4xl text-3xl font-bold md:text-5xl">
            Not a broker. Not an advisor. Not a hype machine.
          </h2>

          <p className="mt-6 max-w-3xl leading-8 text-slate-400">
            PressureTest is an educational diligence platform designed to help
            users slow down, structure their review, and identify pressure before
            signing, financing, leasing, hiring, or committing capital.
          </p>
        </div>
      </section>
    </main>
  );
}