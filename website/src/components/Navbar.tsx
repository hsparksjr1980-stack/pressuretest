import Link from "next/link";

export default function Navbar() {
  return (
    <nav className="sticky top-0 z-50 border-b border-white/10 bg-[#070a0d]/70 backdrop-blur-2xl">
      <div className="mx-auto flex max-w-6xl items-center justify-between gap-6 px-6 py-3">
        <Link href="/" className="flex items-center gap-3">
          <span
            aria-hidden="true"
            className="glass-panel-soft relative grid h-10 w-10 place-items-center rounded-full"
          >
            <span className="absolute h-7 w-7 rounded-full border-[5px] border-slate-700 border-r-red-500 border-t-amber-300" />
            <span className="absolute h-1 w-4 origin-left rotate-[-38deg] rounded-full bg-red-400" />
            <span className="relative h-2.5 w-2.5 rounded-full bg-white" />
          </span>
          <span className="text-lg font-black italic tracking-normal text-slate-100">
            Pressure<span className="text-red-500">Test</span>
          </span>
        </Link>

        <div className="hidden items-center gap-7 text-sm text-slate-300 md:flex">
          <Link href="/how-it-works" className="hover:text-white">
            How It Works
          </Link>

          <Link href="/pricing" className="hover:text-white">
            Pricing
          </Link>

          <Link href="/blog" className="hover:text-white">
            Blog
          </Link>

          <Link href="/privacy" className="hover:text-white">
            Privacy
          </Link>
        </div>

        <Link
          href="/contact"
          className="rounded-lg border border-white/15 bg-white/5 px-4 py-2.5 text-sm font-semibold text-white backdrop-blur-xl transition hover:border-red-300/70 hover:bg-white/10"
        >
          Join Waitlist
        </Link>
      </div>
    </nav>
  );
}
