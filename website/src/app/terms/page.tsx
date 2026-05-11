export default function TermsPage() {
  return (
    <main className="min-h-screen bg-[#0b0f14] px-6 py-20 text-white">
      <section className="mx-auto max-w-4xl">
        <p className="mb-4 text-sm uppercase tracking-[0.3em] text-slate-500">
          Terms of Use
        </p>

        <h1 className="text-5xl font-bold leading-tight md:text-6xl">
          Terms of Use
        </h1>

        <p className="mt-6 text-slate-400">Last updated: May 11, 2026</p>

        <div className="mt-12 space-y-10 leading-8 text-slate-300">
          {[
            ["Platform Purpose", "PressureTest is an educational diligence and operational planning platform designed to help users organize assumptions, review operational pressure points, and prepare for business ownership decisions."],
            ["No Professional Advice", "PressureTest does not provide legal, financial, tax, accounting, lending, investment, franchise advisory, or brokerage services."],
            ["User Responsibility", "Users are responsible for independently validating all assumptions, reviewing source materials, and consulting qualified professionals before making business decisions."],
            ["No Guarantees", "PressureTest does not guarantee business outcomes, predict success or failure, endorse franchise systems, or recommend any specific investment or transaction."],
            ["Educational Outputs", "Reports, calculators, workflows, and summaries are provided for educational and planning purposes only."],
            ["Working Draft Notice", "These Terms of Use are a working draft and should be reviewed by qualified counsel before public launch."],
          ].map(([title, body]) => (
            <section key={title}>
              <h2 className="mb-3 text-2xl font-semibold text-white">{title}</h2>
              <p>{body}</p>
            </section>
          ))}
        </div>
      </section>
    </main>
  );
}