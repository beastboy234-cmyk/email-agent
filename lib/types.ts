export type CostBreakdown = {
  hotel: number; hotelTaxes: number; resortFees: number; parking: number; gasOrAirfare: number;
  baggageFees: number; rentalCar: number; food: number; activities: number; petFees: number; tolls: number; emergencyBuffer: number;
};

export type TripOption = {
  id: string; title: string; destination: string; summary: string; missionReadyScore: number; estimatedRealTripCost: number;
  costBreakdown: CostBreakdown; transportRecommendation: string; hotelRecommendation: string; rentalCarRecommendation: string;
  dailyItinerary: string[]; activities: string[]; hiddenCostWarnings: string[]; familyStressWarnings: string[];
  pros: string[]; cons: string[]; whySelected: string; bookingUrl: string; leaveMode?: { travelDayPlan: string; returnBuffer: string; backupPlan: string; riskWarnings: string[]; refundableRecommendation: string; drivingVsFlying: string; };
};

export type DestinationPackage = { id: string; name: string; description: string; options: TripOption[]; };
