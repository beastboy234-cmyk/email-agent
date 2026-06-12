"use client";
import { useState } from "react";
import { useRouter } from "next/navigation";
const fields = ["Departure city or airport", "Destination or open-to-anywhere", "Travel dates", "Children’s ages", "Total budget", "Hotel preference", "Special notes"];
export function FamilyPlannerForm() {
  const router = useRouter();
  const [form, setForm] = useState<Record<string, string>>({ adults: "2", children: "2", style: "best value", travel: "either" });
  const set = (k: string, v: string) => setForm((f) => ({ ...f, [k]: v }));
  return <form className="card p-6" onSubmit={(e) => { e.preventDefault(); router.push("/results?mode=family"); }}>
    <div className="grid gap-5 md:grid-cols-2">{fields.map((f) => <label className="grid gap-2" key={f}><span className="label">{f}</span><input className="input" value={form[f] ?? ""} onChange={(e) => set(f, e.target.value)} placeholder={f} /></label>)}
      <Select label="Flexible dates" value={form.flex ?? "yes"} onChange={(v) => set("flex", v)} options={["yes", "no"]} />
      <label className="grid gap-2"><span className="label">Number of adults</span><input className="input" type="number" value={form.adults} onChange={(e) => set("adults", e.target.value)} /></label>
      <label className="grid gap-2"><span className="label">Number of children</span><input className="input" type="number" value={form.children} onChange={(e) => set("children", e.target.value)} /></label>
      <Select label="Flying, driving, or either" value={form.travel} onChange={(v) => set("travel", v)} options={["flying", "driving", "either"]} />
      <Select label="Need rental car" value={form.rental ?? "no"} onChange={(v) => set("rental", v)} options={["yes", "no"]} />
      <Select label="Need kid-friendly activities" value={form.kids ?? "yes"} onChange={(v) => set("kids", v)} options={["yes", "no"]} />
      <Select label="Need pet-friendly options" value={form.pets ?? "no"} onChange={(v) => set("pets", v)} options={["yes", "no"]} />
      <Select label="Need refundable options" value={form.refundable ?? "yes"} onChange={(v) => set("refundable", v)} options={["yes", "no"]} />
      <Select label="Preferred travel style" value={form.style} onChange={(v) => set("style", v)} options={["budget", "best value", "comfort", "resort", "adventure", "cruise", "road trip"]} />
    </div><button className="btn-primary mt-6" type="submit">Generate 3 Trip Options</button>
  </form>;
}
function Select({ label, value, onChange, options }: { label: string; value: string; onChange: (v: string) => void; options: string[] }) { return <label className="grid gap-2"><span className="label">{label}</span><select className="input" value={value} onChange={(e) => onChange(e.target.value)}>{options.map((o) => <option key={o}>{o}</option>)}</select></label>; }
