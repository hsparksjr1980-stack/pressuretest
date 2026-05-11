const articles = [
  {
    title: "How Much Working Capital Do New Franchise Owners Actually Need?",
    category: "Cash Flow",
    description:
      "Why startup cost estimates often fail to reflect real operating pressure during ramp.",
  },
  {
    title: "What First-Time Franchise Buyers Underestimate",
    category: "Operations",
    description:
      "Common execution realities that look manageable on paper but become operational pressure quickly.",
  },
  {
    title: "Pressure Testing Revenue Assumptions Before Signing",
    category: "Diligence",
    description:
      "How to evaluate whether revenue projections are realistic before committing capital.",
  },
];

export default function BlogPage() {
  return (
    <main className="min-h-screen bg-[#0b0f14] px-6 py-20 text-white">
      <section className="mx-auto max-w-6xl">
        <p className="mb-4 text-sm uppercase tracking-[0.3em] text-slate-500">
          Insights & Diligence Guides
        </p>

        <h1 className="max-w-4xl text-5xl font-bold leading-tight md:text-7xl">
          Practical content for prospective operators.
        </h1>

        <p className="mt-8 max-w-2xl text-lg leading-8 text-slate-300">
          PressureTest content focuses on operational preparation, diligence
          structure, assumption validation, and execution realities.
        </p>

        <div className="mt-16 grid gap-6">
          {articles.map((article) => (
            <article
              key={article.title}
              className="rounded-2xl border border-slate-800 bg-slate-950 p-8"
            >
              <p className="mb-3 text-sm uppercase tracking-[0.25em] text-slate-500">
                {article.category}
              </p>

              <h2 className="text-3xl font-semibold">{article.title}</h2>

              <p className="mt-4 max-w-3xl leading-8 text-slate-400">
                {article.description}
              </p>

              <a
                href="#"
                className="mt-6 inline-block text-sm font-semibold text-white hover:text-slate-300"
              >
                Read Article →
              </a>
            </article>
          ))}
        </div>
      </section>
    </main>
  );
}