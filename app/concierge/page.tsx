import { ConciergeForm } from "@/components/ConciergeForm";
import { SectionHeader } from "@/components/SectionHeader";
export default function ConciergePage() { return <section className="section"><SectionHeader eyebrow="Concierge Planning" title="Want a real person to review this before you book?" description="Submit a $149 concierge planning request placeholder. Future versions will connect this to Supabase and hosted checkout." /><ConciergeForm /></section>; }
