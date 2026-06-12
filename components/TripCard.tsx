import Link from "next/link";
import type { TripOption } from "@/lib/types";
import { CostBreakdown, formatMoney } from "./CostBreakdown";
import { ScoreBadge } from "./ScoreBadge";

export function TripCard({ trip, compact = false }: { trip: TripOption; compact?: boolean }) {
  return <article className="card overflow-hidden p-5">
    <div className="flex flex-col gap-5 md:flex-row md:items-start md:justify-between">
      <div><p className="badge bg-navy/10 text-navy">{trip.title}</p><h3 className="mt-3 text-2xl font-black text-navy">{trip.destination}</h3><p className="mt-2 text-slate-600">{trip.summary}</p><p className="mt-4 text-3xl font-black text-mission">{formatMoney(trip.estimatedRealTripCost)} <span className="text-sm font-semibold text-slate-500">estimated</span></p></div>
      <ScoreBadge score={trip.missionReadyScore} />
    </div>
    <div className="mt-6 grid gap-5 lg:grid-cols-2"><CostBreakdown costs={trip.costBreakdown} /><div className="space-y-3 text-sm"><p><strong>Travel:</strong> {trip.transportRecommendation}</p><p><strong>Hotel:</strong> {trip.hotelRecommendation}</p><p><strong>Rental car:</strong> {trip.rentalCarRecommendation}</p>{trip.leaveMode && <div className="rounded-2xl border border-mission/20 bg-mission/5 p-4"><p><strong>Travel day plan:</strong> {trip.leaveMode.travelDayPlan}</p><p><strong>Return buffer:</strong> {trip.leaveMode.returnBuffer}</p><p><strong>Backup plan:</strong> {trip.leaveMode.backupPlan}</p><p><strong>Refundable booking:</strong> {trip.leaveMode.refundableRecommendation}</p><p><strong>Drive vs. fly:</strong> {trip.leaveMode.drivingVsFlying}</p></div>}</div></div>
    {!compact && <div className="mt-6 grid gap-5 md:grid-cols-3"><List title="Daily itinerary" items={trip.dailyItinerary} /><List title="Hidden cost warnings" items={trip.hiddenCostWarnings} warning /><List title="Family stress warnings" items={trip.familyStressWarnings} warning /></div>}
    <div className="mt-6 grid gap-5 md:grid-cols-3"><List title="Pros" items={trip.pros} /><List title="Cons" items={trip.cons} /><div className="rounded-2xl bg-sand p-4"><h4 className="font-black text-navy">Why AI selected this</h4><p className="mt-2 text-sm text-slate-700">{trip.whySelected}</p></div></div>
    <div className="mt-6 flex flex-wrap gap-3"><Link className="btn-primary" href={trip.bookingUrl}>Booking Link Placeholder</Link><Link className="btn-secondary" href="/saved-trips">Save Trip</Link><Link className="btn-secondary" href="/compare">Compare Trip</Link><Link className="btn-secondary" href="/concierge">Want a real person to review this before you book?</Link></div>
  </article>;
}
function List({ title, items, warning }: { title: string; items: string[]; warning?: boolean }) { return <div className={`rounded-2xl p-4 ${warning ? "bg-red-50" : "bg-slate-50"}`}><h4 className="font-black text-navy">{title}</h4><ul className="mt-2 space-y-2 text-sm text-slate-700">{items.map((item) => <li key={item}>• {item}</li>)}</ul></div>; }
