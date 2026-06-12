import type { CostBreakdown as CostBreakdownType } from "@/lib/types";
const labels: Record<keyof CostBreakdownType, string> = { hotel: "Hotel price", hotelTaxes: "Hotel taxes", resortFees: "Resort fees", parking: "Parking", gasOrAirfare: "Gas or airfare", baggageFees: "Baggage fees", rentalCar: "Rental car", food: "Food estimate", activities: "Activity estimate", petFees: "Pet fees", tolls: "Tolls", emergencyBuffer: "Emergency buffer" };
const money = (n: number) => new Intl.NumberFormat("en-US", { style: "currency", currency: "USD", maximumFractionDigits: 0 }).format(n);
export function CostBreakdown({ costs }: { costs: CostBreakdownType }) {
  return <div className="rounded-2xl bg-slate-50 p-4"><h4 className="font-black text-navy">Estimated Real Trip Cost</h4><p className="text-xs text-slate-500">All prices are estimates until confirmed by the travel provider.</p><dl className="mt-3 grid grid-cols-2 gap-2 text-sm">{Object.entries(costs).map(([key, value]) => <div className="flex justify-between gap-2 border-b border-slate-200 py-1" key={key}><dt>{labels[key as keyof CostBreakdownType]}</dt><dd className="font-bold">{money(value)}</dd></div>)}</dl></div>;
}
export const formatMoney = money;
