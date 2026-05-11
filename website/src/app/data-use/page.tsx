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
          {[
            [
              "Purpose of Data Use",
              "PressureTest uses user-provided information to help structure diligence workflows, organize assumptions, review operational readiness, and generate educational planning outputs.",
            ],
            [
              "User Inputs",
              "Users may voluntarily enter assumptions related to startup costs, working capital, staffing, revenue expectations, operating risks, and execution timelines.",
            ],
            [
              "Educational Outputs",
              "PressureTest may use submitted information to generate summaries, calculators, workflows, operational reviews, or educational reporting outputs.",
            ],
            [
              "Analytics & Improvement",
              "Usage patterns and platform interactions may be reviewed to improve workflows, usability, navigation, educational content, and product functionality.",
            ],
            [
              "No Outcome Prediction",
              "PressureTest does not guarantee outcomes, validate assumptions, predict success, or replace independent diligence and professional review.",
            ],
            [
              "Third-Party Services",
              "PressureTest may rely on third-party infrastructure, hosting, analytics, and software providers to support operation of the platform.",
            ],
            [
              "Working Draft Notice",
              "This Data Use page is a working draft and should be reviewed by qualified counsel before public launch.",
            ],
          ].map(([title, body]) => (
            <section key={title}>
              <h2 className="mb-3 text-2xl font-semibold text-white">
                {title}
              </h2>

              <p>{body}</p>
            </section>
          ))}
        </div>
      </section>
    </main>
  );
}