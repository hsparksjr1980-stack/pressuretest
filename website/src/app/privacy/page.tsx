export default function PrivacyPage() {
  return (
    <main className="min-h-screen bg-[#0b0f14] px-6 py-20 text-white">
      <section className="mx-auto max-w-4xl">
        <p className="mb-4 text-sm uppercase tracking-[0.3em] text-slate-500">
          Privacy Policy
        </p>

        <h1 className="text-5xl font-bold leading-tight md:text-6xl">
          Privacy Policy
        </h1>

        <p className="mt-6 text-slate-400">Last updated: May 11, 2026</p>

        <div className="mt-12 space-y-10 leading-8 text-slate-300">
          <section>
            <h2 className="mb-3 text-2xl font-semibold text-white">Overview</h2>
            <p>
              PressureTest is designed as an educational diligence and operational
              planning tool. This page explains how information may be collected,
              used, and protected when users interact with the platform.
            </p>
          </section>

          <section>
            <h2 className="mb-3 text-2xl font-semibold text-white">
              Information We May Collect
            </h2>
            <p>
              We may collect information users voluntarily provide, such as name,
              email address, business evaluation details, form responses, waitlist
              submissions, and inputs entered into diligence tools or calculators.
            </p>
          </section>

          <section>
            <h2 className="mb-3 text-2xl font-semibold text-white">
              How Information May Be Used
            </h2>
            <p>
              Information may be used to operate the platform, improve product
              functionality, respond to inquiries, provide educational outputs,
              support waitlist communication, and improve diligence workflows.
            </p>
          </section>

          <section>
            <h2 className="mb-3 text-2xl font-semibold text-white">
              Working Draft Notice
            </h2>
            <p>
              This page is a working draft and should be reviewed by qualified
              counsel before public launch.
            </p>
          </section>
        </div>
      </section>
    </main>
  );
}