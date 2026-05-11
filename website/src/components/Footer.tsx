export default function Footer() {
  return (
    <footer className="border-t border-slate-800 bg-[#0b0f14] px-6 py-12 text-white">
      <div className="mx-auto flex max-w-6xl flex-col gap-10 md:flex-row md:justify-between">
        <div className="max-w-sm">
          <h3 className="text-lg font-semibold">PressureTest</h3>

          <p className="mt-4 text-sm leading-7 text-slate-400">
            Structured diligence and operational planning for prospective
            franchise and small-business operators.
          </p>
        </div>

        <div className="grid grid-cols-2 gap-10 text-sm md:grid-cols-3">
          <div>
            <p className="mb-4 font-semibold text-white">Platform</p>

            <div className="space-y-3 text-slate-400">
              <a href="/" className="block hover:text-white">
                Home
              </a>

              <a href="/how-it-works" className="block hover:text-white">
                How It Works
              </a>

              <a href="/pricing" className="block hover:text-white">
                Pricing
              </a>

              <a href="/blog" className="block hover:text-white">
                Blog
              </a>
            </div>
          </div>

          <div>
            <p className="mb-4 font-semibold text-white">Legal</p>

            <div className="space-y-3 text-slate-400">
              <a href="/privacy" className="block hover:text-white">
                Privacy
              </a>

              <a href="/data-use" className="block hover:text-white">
                Data Use
              </a>

              <a href="/terms" className="block hover:text-white">
                Terms
              </a>

              <a href="/disclaimer" className="block hover:text-white">
                Disclaimer
              </a>
            </div>
          </div>

          <div>
            <p className="mb-4 font-semibold text-white">Content</p>

            <div className="space-y-3 text-slate-400">
              <a
                href="/blog/what-first-time-franchise-buyers-underestimate"
                className="block hover:text-white"
              >
                First-Time Buyers
              </a>

              <a
                href="/blog/how-much-working-capital-do-new-franchise-owners-need"
                className="block hover:text-white"
              >
                Working Capital
              </a>

              <a
                href="/blog/pressure-testing-revenue-assumptions-before-signing"
                className="block hover:text-white"
              >
                Revenue Assumptions
              </a>
            </div>
          </div>
        </div>
      </div>

      <div className="mx-auto mt-12 max-w-6xl border-t border-slate-800 pt-6 text-sm text-slate-500">
        © 2026 PressureTest. Educational diligence platform.
      </div>
    </footer>
  );
}