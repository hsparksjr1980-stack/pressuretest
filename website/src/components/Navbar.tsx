export default function Navbar() {
  return (
    <nav className="mx-auto flex max-w-6xl items-center justify-between border-b border-slate-800 bg-[#0b0f14] px-6 py-6">
      <a href="/" className="text-lg font-semibold tracking-tight text-white">
        PressureTest
      </a>

      <div className="flex gap-6 text-sm text-slate-300">
        <a href="/how-it-works" className="hover:text-white">
          How It Works
        </a>

        <a href="/pricing" className="hover:text-white">
          Pricing
        </a>

        <a href="/blog" className="hover:text-white">
          Blog
        </a>

        <a href="/contact" className="hover:text-white">
          Contact
        </a>
      </div>

      <a
        href="/contact"
        className="rounded-lg border border-slate-700 px-4 py-2 text-sm font-medium text-slate-200 hover:border-slate-500"
      >
        Join Waitlist
      </a>
    </nav>
  );
}