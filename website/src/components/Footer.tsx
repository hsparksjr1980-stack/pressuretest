export default function Footer() {
  return (
    <footer className="border-t border-slate-800 bg-[#0b0f14] px-6 py-12 text-white">
      <div className="mx-auto flex max-w-6xl flex-col gap-10 md:flex-row md:justify-between">
        <div className="max-w-md">
          <h3 className="text-lg font-semibold">PressureTest</h3>

          <p className="mt-4 text-sm leading-7 text-slate-400">
            Structured franchise and small-business diligence focused on
            operational preparation, financial pressure testing, and execution
            realism.
          </p>
        </div>

        <div className="grid grid-cols-2 gap-10 text-sm md:grid-cols-3">
          <div>
            <h4 className="mb-4 font-semibold text-white">Platform</h4>

            <div className="space-y-3 text-slate-400">
              <a href="/" className="block hover:text-white">
                Home
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
            <h4 className="mb-4 font-semibold text-white">Resources</h4>

            <div className="space-y-3 text-slate-400">
              <a href="/how-it-works" className="block hover:text-white">
                How It Works
              </a>

              <a href="/privacy" className="block hover:text-white">
                Privacy
              </a>

              <a href="/data-use" className="block hover:text-white">
                Data Use
              </a>
            </div>
          </div>

          <div>
            <h4 className="mb-4 font-semibold text-white">Legal</h4>

            <div className="space-y-3 text-slate-400">
              <a href="/disclaimer" className="block hover:text-white">
                Disclaimer
              </a>

              <a href="/terms" className="block hover:text-white">
                Terms
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