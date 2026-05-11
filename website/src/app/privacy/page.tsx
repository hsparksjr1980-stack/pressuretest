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
          {[
            [
              "Overview",
              "PressureTest is an educational diligence and operational planning platform. This page explains how information may be collected, used, and protected when users interact with the platform.",
            ],
            [
              "Information We May Collect",
              "We may collect information voluntarily provided by users, including names, email addresses, waitlist submissions, questionnaire responses, calculator inputs, and diligence-related assumptions.",
            ],
            [
              "How Information May Be Used",
              "Information may be used to operate the platform, improve workflows, respond to inquiries, provide educational outputs, improve usability, and support future product development.",
            ],
            [
              "Data Storage",
              "PressureTest may use third-party hosting, analytics, infrastructure, and software providers to support operation of the platform.",
            ],
            [
              "No Sale of Personal Information",
              "PressureTest does not currently intend to sell personal information to third parties.",
            ],
            [
              "User Responsibility",
              "Users should avoid submitting sensitive personal, financial, legal, medical, or confidential business information unless specifically requested through secure workflows.",
            ],
            [
              "Working Draft Notice",
              "This Privacy Policy is a working draft and should be reviewed by qualified counsel before public launch.",
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