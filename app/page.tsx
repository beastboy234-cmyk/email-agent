import Link from "next/link";
import { PricingCards } from "@/components/PricingCards";
import { SectionHeader } from "@/components/SectionHeader";
import { TripCard } from "@/components/TripCard";
import { tripOptions } from "@/lib/mock-data";

export default function Home() {
  return <>
    <section className="section grid items-center gap-10 lg:grid-cols-[1.1fr_.9fr]">
      <div><p className="badge bg-navy text-white">AI family travel decision system</p><h1 className="mt-5 text-5xl font-black tracking-tight text-navy sm:text-6xl">Family travel planned with military precision.</h1><p className="mt-6 text-xl text-slate-700">Mission Ready Vacations AI helps military families and busy families compare affordable trip options, estimate real costs, avoid hidden fees, and build smarter vacations around real schedules.</p><div className="mt-8 flex flex-wrap gap-3"><Link className="btn-primary" href="/planner">Plan My Vacation</Link><Link className="btn-secondary" href="/leave-mode">Build My Leave Trip</Link></div></div>
      <div className="card p-5"><TripCard trip={tripOptions[1]} compact /></div>
    </section>
    <section className="section"><SectionHeader eyebrow="How it works" title="Structured planning instead of a blank chatbot" description="Answer guided questions, compare three practical options, and understand the real estimated cost before you click a provider placeholder." /><div className="grid gap-5 md:grid-cols-3">{["Tell us your family constraints", "AI scores cost, stress, and logistics", "Compare, save, or upgrade to concierge"].map((x, i) => <div className="card p-6" key={x}><span className="text-4xl font-black text-mission">0{i + 1}</span><h3 className="mt-4 text-xl font-black text-navy">{x}</h3><p className="mt-2 text-slate-600">Designed for budget, kids, pets, leave dates, refundability, and hidden costs.</p></div>)}</div></section>
    <section className="section grid gap-5 md:grid-cols-2"><Info title="Family travel benefits" items={["Kid-friendly pacing", "Food and activity estimates", "Pet-friendly and refundable filters", "Stress warnings that parents can act on"]} /><Info title="Military family travel benefits" items={["Leave Mode return buffers", "Duty-station based planning", "Refundability and backup plans", "Military discount preference without implying government affiliation"]} /></section>
    <section className="section grid gap-5 md:grid-cols-2"><Info title="Mission Ready Score" items={["1-100 practical readiness score", "Budget fit, travel time, comfort, refundability", "Military-family practicality and overall stress"]} /><Info title="Real Total Cost Calculator" items={["Hotel, taxes, resort fees, parking", "Gas/airfare, baggage, rental car", "Food, activities, pets, tolls, emergency buffer"]} /></section>
    <section className="section"><SectionHeader eyebrow="Pricing" title="Start free, upgrade when you want more confidence" /><PricingCards /></section>
    <section className="section"><div className="card bg-red-50 p-6"><h2 className="text-2xl font-black text-navy">Important disclaimer</h2><p className="mt-3 text-slate-700">Mission Ready Vacations AI is not affiliated with the Department of Defense, DTS, DTMO, MWR, American Forces Travel, or any government agency. We do not directly sell travel. All prices are estimates until confirmed by travel providers.</p></div></section>
    <section className="section"><SectionHeader eyebrow="FAQ" title="Questions families ask before booking" /><div className="grid gap-4 md:grid-cols-2">{["Does this book travel? No, it provides planning and placeholder links.", "Are prices final? No, they are estimates until provider confirmation.", "Is this official military travel? No, it is independent family planning.", "Can a person review my plan? Yes, use the concierge request flow."].map((q) => <div className="card p-5" key={q}>{q}</div>)}</div></section>
  </>;
}
function Info({ title, items }: { title: string; items: string[] }) { return <div className="card p-6"><h2 className="text-2xl font-black text-navy">{title}</h2><ul className="mt-4 space-y-2 text-slate-700">{items.map((i) => <li key={i}>✓ {i}</li>)}</ul></div>; }
