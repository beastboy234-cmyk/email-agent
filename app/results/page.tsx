import { SectionHeader } from "@/components/SectionHeader";
import { TripCard } from "@/components/TripCard";
import { leaveModeOptions, tripOptions } from "@/lib/mock-data";
export default function ResultsPage({ searchParams }: { searchParams: { mode?: string } }) { const leave = searchParams.mode === "leave"; const options = leave ? leaveModeOptions : tripOptions; return <section className="section"><SectionHeader eyebrow={leave ? "Leave Mode Results" : "AI Trip Results"} title="Three mission-ready trip options" description="Each card shows a Mission Ready Score, estimated real trip cost, hidden cost warnings, family stress warnings, and the AI rationale." /><div className="space-y-8">{options.map((trip) => <TripCard trip={trip} key={trip.id} />)}</div></section>; }
