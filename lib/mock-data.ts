import type { CostBreakdown, DestinationPackage, TripOption } from "./types";

const breakdown = (base: Partial<CostBreakdown>): CostBreakdown => ({
  hotel: 650, hotelTaxes: 92, resortFees: 0, parking: 60, gasOrAirfare: 260, baggageFees: 0,
  rentalCar: 0, food: 360, activities: 240, petFees: 0, tolls: 25, emergencyBuffer: 175, ...base
});
const total = (c: CostBreakdown) => Object.values(c).reduce((sum, value) => sum + value, 0);
const option = (id: string, title: string, destination: string, score: number, base: Partial<CostBreakdown>, extra?: Partial<TripOption>): TripOption => {
  const costs = breakdown(base);
  return {
    id, title, destination, missionReadyScore: score, estimatedRealTripCost: total(costs), costBreakdown: costs,
    summary: "A structured family plan balancing cost, convenience, schedule risk, and kid-friendly pacing.",
    transportRecommendation: "Drive with one planned meal stop and one playground break to reduce family stress.",
    hotelRecommendation: "Suite-style hotel with breakfast, parking clarity, and flexible cancellation.",
    rentalCarRecommendation: costs.rentalCar > 0 ? "Reserve a midsize SUV through hosted partner checkout placeholder." : "Not needed for this road-trip option.",
    dailyItinerary: ["Day 1: Travel, check in, grocery run, low-key pool time.", "Day 2: Main attraction day with early start and midday rest.", "Day 3: Free/backup morning, family activity, simple dinner.", "Day 4: Pack, checkout, return with buffer before duty/work."],
    activities: ["Children's museum or aquarium", "Outdoor park time", "Low-cost local food stop", "Rainy-day indoor backup"],
    hiddenCostWarnings: ["Prices are estimates until confirmed by provider.", "Confirm parking and resort fees before booking.", "Budget for snacks, tolls, and cancellation changes."],
    familyStressWarnings: ["Cheap choices can add travel burden.", "Avoid late arrivals with tired kids.", "Keep one flexible block for naps, weather, or duty changes."],
    pros: ["Clear real-cost estimate", "Family-friendly pacing", "Refundable lodging recommended"],
    cons: ["Some provider prices may change", "Activities may require advance reservations"],
    whySelected: "The AI selected this option because it fits the stated budget while minimizing hidden fees and return-day risk.",
    bookingUrl: "/api/affiliate/click?provider=placeholder",
    ...extra
  };
};

export const tripOptions: TripOption[] = [
  option("cheap-practical", "Cheapest Practical Option", "Savannah, GA", 82, { hotel: 430, hotelTaxes: 58, parking: 35, gasOrAirfare: 90, food: 260, activities: 120, emergencyBuffer: 120 }, { summary: "Lowest reasonable total cost without choosing a high-stress red-eye, unsafe hotel location, or impossible schedule." }),
  option("best-value", "Best Value Option", "Orlando, FL", 91, { hotel: 720, hotelTaxes: 110, resortFees: 65, parking: 85, gasOrAirfare: 180, food: 420, activities: 360, emergencyBuffer: 220 }, { summary: "Best balance of kid-friendly lodging, manageable drive time, refundable terms, and total estimated cost." }),
  option("comfortable-family", "Most Comfortable Family Option", "Charleston, SC", 88, { hotel: 980, hotelTaxes: 145, parking: 120, gasOrAirfare: 140, rentalCar: 0, food: 520, activities: 420, emergencyBuffer: 260 }, { summary: "Higher comfort plan with larger room, easier logistics, shorter daily transitions, and more rest time." })
];

export const leaveModeOptions: TripOption[] = tripOptions.map((trip, index) => ({
  ...trip,
  id: `leave-${trip.id}`,
  title: ["Leave Cheapest Practical Option", "Leave Best Value Option", "Leave Most Comfortable Family Option"][index],
  leaveMode: {
    travelDayPlan: "Depart early, avoid last-minute duty handoff conflicts, pre-pack documents, and keep a 30-minute fuel buffer.",
    returnBuffer: index === 0 ? "Return the afternoon before duty; acceptable but not ideal." : "Return at least 24 hours before duty/work to protect against weather, car issues, or delayed flights.",
    backupPlan: "Hold a refundable nearby hotel and identify a shorter destination if leave approval changes.",
    riskWarnings: ["Do not schedule the last return leg too close to first formation/work.", "Refundable options reduce risk if leave dates shift.", "Confirm pet and kitchen/laundry policies directly."],
    refundableRecommendation: "Choose refundable lodging and avoid non-changeable tickets until leave is fully approved.",
    drivingVsFlying: index === 1 ? "Driving is recommended for control and lower baggage risk." : "Either can work; compare schedule risk before booking."
  }
}));

export const packages: DestinationPackage[] = [
  "Fort Stewart to Orlando|Theme parks with rest blocks", "Fort Stewart to Savannah|Low-cost coastal weekend", "Fort Stewart to Atlanta|City attractions and aquarium", "Fort Stewart to Gatlinburg|Mountain cabin road trip", "Fort Stewart to Myrtle Beach|Beach value getaway", "Fort Stewart to Charleston|Historic coastal comfort", "Military family beach weekend|Short, refundable, beach-focused plan", "Budget Disney family trip|Off-property value plan with fee warnings", "4-day leave getaway|Protected return buffer plan", "Pet-friendly road trip|Hotel and stop plan for pets"
].map((item, idx) => {
  const [name, description] = item.split("|");
  return { id: name.toLowerCase().replace(/[^a-z0-9]+/g, "-"), name, description, options: tripOptions.map((t, i) => ({ ...t, id: `${idx}-${i}`, destination: name.replace("Fort Stewart to ", "") })) };
});

export const pricingPlans = [
  { name: "Free AI Search", price: "$0", href: "/planner", features: ["Structured trip search", "3 mock AI options", "Mission Ready Score", "Estimated real cost"] },
  { name: "Family Trip Plan", price: "$19", href: "/checkout?plan=family", features: ["Printable itinerary placeholder", "Save and compare trips", "Family stress warnings", "Provider link placeholders"] },
  { name: "Military Family Leave Plan", price: "$49", href: "/checkout?plan=leave", features: ["Leave Mode", "Return buffer recommendation", "Backup plan", "Refundability guidance"] },
  { name: "Concierge Planning", price: "$149", href: "/concierge", features: ["Human review request", "Personalized concern review", "Military-family practical checks", "Hosted checkout placeholder"] }
];

export const adminStats = { totalTripRequests: 1248, familyTripRequests: 846, leaveModeRequests: 402, averageBudget: "$2,180", topDestinations: ["Orlando", "Savannah", "Gatlinburg", "Myrtle Beach"], savedTrips: 318, conciergeRequests: 41, affiliateClicks: 702, paymentStatuses: ["placeholder_succeeded", "placeholder_pending", "not_collected"] };
