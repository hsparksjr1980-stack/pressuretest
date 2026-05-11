const articles = [
  {
    title: "What First-Time Franchise Buyers Underestimate",
    category: "Operations",
    href: "/blog/what-first-time-franchise-buyers-underestimate",
    description:
      "A practical review of staffing, ramp timing, working capital, and execution pressure before signing.",
  },
  {
    title: "How Much Working Capital Do New Franchise Owners Actually Need?",
    category: "Cash Flow",
    href: "/blog/how-much-working-capital-do-new-franchise-owners-need",
    description:
      "Why startup cost estimates rarely tell the full story of cash pressure during the first year.",
  },
  {
    title: "Pressure Testing Revenue Assumptions Before Signing",
    category: "Diligence",
    href: "/blog/pressure-testing-revenue-assumptions-before-signing",
    description:
      "How to slow down optimistic projections and review whether assumptions are grounded.",
  },
];

export default function BlogPage() {
  return (
    <main className="min-h-screen bg-[#0b0f14] px-6 py-20 text-white">
      <section className="mx-auto max-w-6xl">
        <p className="mb-4 text-sm uppercase tracking-[0.3em] text-slate-500">
          PressureTest Library
        </p>

        <h1 className="max-w-4xl text-5xl font-bold leading-tight md:text-7xl">
          Practical diligence content for prospective operators.
        </h1>

        <p className="mt-8 max-w-3xl text-lg leading-8 text-slate-300">
          Guides focused on operational preparation, financial pressure,
          assumption review, and decision readiness before committing capital.
        </p>

        <div className="mt-16 grid gap-6">
          {articles.map((article) => (
            <a
              key={article.title}
              href={article.href}
              className="block rounded-2xl border border-slate-800 bg-slate-950 p-8 hover:border-slate-600"
            >
              <p className="mb-3 text-sm uppercase tracking-[0.25em] text-slate-500">
                {article.category}
              </p>

              <h2 className="text-3xl font-semibold">{article.title}</h2>

              <p className="mt-4 max-w-3xl leading-8 text-slate-400">
                {article.description}
              </p>

              <p className="mt-6 text-sm font-semibold text-white">
                Read guide →
              </p>
            </a>
          ))}
        </div>
      </section>
    </main>
  );
}