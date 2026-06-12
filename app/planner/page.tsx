import { FamilyPlannerForm } from "@/components/FamilyPlannerForm";
import { SectionHeader } from "@/components/SectionHeader";
export default function PlannerPage() { return <section className="section"><SectionHeader eyebrow="Family Trip Planner" title="Plan around real family constraints" description="No blank chatbot. Use a structured planning form to generate three practical trip options." /><FamilyPlannerForm /></section>; }
