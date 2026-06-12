import { PricingCards } from "@/components/PricingCards";
import { SectionHeader } from "@/components/SectionHeader";
export default function PricingPage() { return <section className="section"><SectionHeader eyebrow="Pricing" title="Simple planning plans with hosted checkout placeholders" description="We do not collect credit card data directly. Paid plans route to Stripe or PayPal hosted checkout placeholders." /><PricingCards /></section>; }
