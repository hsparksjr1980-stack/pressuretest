import Image from "next/image";

export default function Navbar() {
  return (
    <nav className="border-b border-slate-200 bg-white">
      <div className="mx-auto flex max-w-6x1 items-center justify-between px-6 py-0">
        <a href="/" className="flex items-center">
          <Image
            src="/logo.png"
            alt="PressureTest"
            width={300}
            height={70}
            priority
            className="max-h-35 w-auto object-contain"
          />
        </a>

        <div className="hidden items-center gap-8 text-sm text-slate-600 md:flex">
          <a href="/how-it-works" className="hover:text-black">
            How It Works
          </a>

          <a href="/pricing" className="hover:text-black">
            Pricing
          </a>

          <a href="/blog" className="hover:text-black">
            Blog
          </a>

          <a href="/privacy" className="hover:text-black">
            Privacy
          </a>
        </div>

        <a
          href="/contact"
          className="rounded-xl border border-slate-300 px-5 py-2.5 text-sm font-medium text-black hover:border-slate-500"
        >
          Join Waitlist
        </a>
      </div>
    </nav>
  );
}