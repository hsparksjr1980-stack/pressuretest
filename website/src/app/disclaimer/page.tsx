export default function DisclaimerPage() {
  return (
    <main className="min-h-screen bg-[#0b0f14] px-6 py-20 text-white">
      <section className="mx-auto max-w-4xl">
        <p className="mb-4 text-sm uppercase tracking-[0.3em] text-slate-500">
          Disclaimer
        </p>

        <h1 className="text-5xl font-bold leading-tight md:text-6xl">
          Educational Use Disclaimer
        </h1>

        <p className="mt-6 text-slate-400">Last updated: May 11, 2026</p>

        <div className="mt-12 space-y-10 leading-8 text-slate-300">
          {[
            ["Educational Purpose", "PressureTest is designed for educational diligence, operational planning, and assumption review. It is intended to help users think more clearly about business pressure points before committing capital."],
            ["Not Professional Advice", "PressureTest does not provide legal, financial, tax, accounting, lending, investment, franchise advisory, or brokerage advice."],
            ["No Recommendations", "PressureTest does not recommend, endorse, rank, approve, or reject any franchise system, business opportunity, investment, lender, broker, advisor, or transaction."],
            ["No Guarantees", "PressureTest does not guarantee outcomes, profitability, financing approval, operational success, risk reduction, or investment performance."],
            ["User Responsibility", "Users should independently verify all assumptions, review source documents, conduct diligence, and consult qualified professionals before making business decisions."],
            ["Working Draft Notice", "This disclaimer is a working draft and should be reviewed by qualified counsel before public launch."],
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