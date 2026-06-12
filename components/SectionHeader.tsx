export function SectionHeader({ eyebrow, title, description }: { eyebrow?: string; title: string; description?: string }) {
  return <div className="mx-auto mb-10 max-w-3xl text-center">{eyebrow && <p className="badge bg-mission/10 text-mission">{eyebrow}</p>}<h2 className="mt-4 text-3xl font-black tracking-tight text-navy sm:text-4xl">{title}</h2>{description && <p className="mt-4 text-lg text-slate-600">{description}</p>}</div>;
}
