"use client";
import { useState } from "react";
import { useRouter } from "next/navigation";
export function LeaveModeForm() {
  const router = useRouter();
  const [form, setForm] = useState<Record<string, string>>({ branch: "Army", travel: "driving", discounts: "yes", refundable: "yes" });
  const set = (k: string, v: string) => setForm((f) => ({ ...f, [k]: v }));
  const inputs = ["Duty station or current city", "Leave start date", "Leave end date", "Travel radius", "Family size", "Kids’ ages", "Budget", "Need hotel near base, airport, or attraction", "Return buffer preference", "Special notes"];
  return <form className="card p-6" onSubmit={(e) => { e.preventDefault(); router.push("/results?mode=leave"); }}>
    <div className="grid gap-5 md:grid-cols-2">{inputs.map((f) => <label className="grid gap-2" key={f}><span className="label">{f}</span><input className="input" value={form[f] ?? ""} onChange={(e) => set(f, e.target.value)} placeholder={f} /></label>)}
      <Select label="Branch" value={form.branch} onChange={(v) => set("branch", v)} options={["Army", "Navy", "Air Force", "Marine Corps", "Space Force", "Coast Guard", "National Guard", "Reserve"]} />
      <Select label="Flying, driving, or either" value={form.travel} onChange={(v) => set("travel", v)} options={["flying", "driving", "either"]} />
      <Select label="Need pet-friendly hotel" value={form.pet ?? "no"} onChange={(v) => set("pet", v)} options={["yes", "no"]} />
      <Select label="Need kitchen/laundry" value={form.kitchen ?? "yes"} onChange={(v) => set("kitchen", v)} options={["yes", "no"]} />
      <Select label="Need refundable options" value={form.refundable} onChange={(v) => set("refundable", v)} options={["yes", "no"]} />
      <Select label="Military discount preference" value={form.discounts} onChange={(v) => set("discounts", v)} options={["yes", "no"]} />
    </div><button className="btn-primary mt-6" type="submit">Build Leave Trip</button>
  </form>;
}
function Select({ label, value, onChange, options }: { label: string; value: string; onChange: (v: string) => void; options: string[] }) { return <label className="grid gap-2"><span className="label">{label}</span><select className="input" value={value} onChange={(e) => onChange(e.target.value)}>{options.map((o) => <option key={o}>{o}</option>)}</select></label>; }
