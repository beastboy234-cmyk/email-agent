import Link from "next/link";
import { pricingPlans } from "@/lib/mock-data";
export function PricingCards() { return <div className="grid gap-5 md:grid-cols-2 lg:grid-cols-4">{pricingPlans.map((plan) => <div className="card p-6" key={plan.name}><h3 className="text-xl font-black text-navy">{plan.name}</h3><p className="mt-3 text-4xl font-black text-mission">{plan.price}</p><ul className="mt-5 space-y-2 text-sm text-slate-600">{plan.features.map((f) => <li key={f}>✓ {f}</li>)}</ul><Link className="btn-primary mt-6 w-full" href={plan.href}>Choose plan</Link></div>)}</div>; }
