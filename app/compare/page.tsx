import Link from "next/link";
import { SectionHeader } from "@/components/SectionHeader";
import { TripCard } from "@/components/TripCard";
import { tripOptions } from "@/lib/mock-data";
export default function ComparePage() { return <section className="section"><SectionHeader eyebrow="Trip Comparison Dashboard" title="Compare cost, score, stress, and logistics side by side" description="MVP dashboard for saved trips, booking placeholders, PDF export placeholders, spouse email placeholders, and concierge upgrades." /><div className="mb-6 flex flex-wrap gap-3"><button className="btn-secondary">Export itinerary to PDF placeholder</button><button className="btn-secondary">Email trip plan to spouse/family placeholder</button><Link className="btn-primary" href="/concierge">Upgrade to concierge planning</Link></div><div className="grid gap-6 xl:grid-cols-3">{tripOptions.map((trip) => <TripCard trip={trip} compact key={trip.id} />)}</div></section>; }
