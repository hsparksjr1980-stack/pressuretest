import Link from "next/link";

export default function Footer() {
  return (
    <footer className="border-t border-white/10 bg-[#070a0d]/90 px-6 py-12 text-white">
      <div className="mx-auto flex max-w-6xl flex-col gap-10 md:flex-row md:justify-between">
        <div className="max-w-sm">
          <h3 className="text-lg font-semibold">PressureTest: Franchise</h3>

          <p className="mt-4 text-sm leading-7 text-slate-400">
            Educational diligence software for prospective franchise operators
            before they sign, borrow, lease, or invest.
          </p>
        </div>

        <div className="grid grid-cols-2 gap-10 text-sm md:grid-cols-3">
          <div>
            <p className="mb-4 font-semibold text-white">Platform</p>

            <div className="space-y-3 text-slate-400">
              <Link href="/" className="block hover:text-white">
                Home
              </Link>

              <Link href="/how-it-works" className="block hover:text-white">
                How It Works
              </Link>

              <Link href="/pricing" className="block hover:text-white">
                Pricing
              </Link>

              <Link href="/blog" className="block hover:text-white">
                Blog
              </Link>
            </div>
          </div>

          <div>
            <p className="mb-4 font-semibold text-white">Legal</p>

            <div className="space-y-3 text-slate-400">
              <Link href="/privacy" className="block hover:text-white">
                Privacy
              </Link>

              <Link href="/data-use" className="block hover:text-white">
                Data Use
              </Link>

              <Link href="/terms" className="block hover:text-white">
                Terms
              </Link>

              <Link href="/disclaimer" className="block hover:text-white">
                Disclaimer
              </Link>
            </div>
          </div>

          <div>
            <p className="mb-4 font-semibold text-white">Content</p>

            <div className="space-y-3 text-slate-400">
              <Link
                href="/blog/what-first-time-franchise-buyers-underestimate"
                className="block hover:text-white"
              >
                First-Time Buyers
              </Link>

              <Link
                href="/blog/how-much-working-capital-do-new-franchise-owners-need"
                className="block hover:text-white"
              >
                Working Capital
              </Link>

              <Link
                href="/blog/pressure-testing-revenue-assumptions-before-signing"
                className="block hover:text-white"
              >
                Revenue Assumptions
              </Link>
            </div>
          </div>
        </div>
      </div>

      <div className="mx-auto mt-12 max-w-6xl border-t border-white/10 pt-6 text-sm text-slate-500">
        © 2026 PressureTest. Educational diligence software. Not legal, tax,
        accounting, lending, financial, or investment advice.
      </div>
    </footer>
  );
}
