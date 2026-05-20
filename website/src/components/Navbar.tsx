import Image from "next/image";
import Link from "next/link";

export default function Navbar() {
  return (
    <nav className="border-b border-slate-200 bg-white">
      <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-0">
        <Link href="/" className="flex items-center">
          <Image
            src="/logo.png"
            alt="PressureTest"
            width={300}
            height={70}
            priority
            className="max-h-35 w-auto object-contain"
          />
        </Link>

        <div className="hidden items-center gap-8 text-sm text-slate-600 md:flex">
          <Link href="/how-it-works" className="hover:text-black">
            How It Works
          </Link>

          <Link href="/pricing" className="hover:text-black">
            Pricing
          </Link>

          <Link href="/blog" className="hover:text-black">
            Blog
          </Link>

          <Link href="/privacy" className="hover:text-black">
            Privacy
          </Link>
        </div>

        <Link
          href="/contact"
          className="rounded-xl border border-slate-300 px-5 py-2.5 text-sm font-medium text-black hover:border-slate-500"
        >
          Join Waitlist
        </Link>
      </div>
    </nav>
  );
}
