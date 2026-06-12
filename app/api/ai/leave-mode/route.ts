import { NextResponse } from "next/server";
import { leaveModeOptions } from "@/lib/mock-data";

export async function POST() {
  // Future OpenAI integration: use Leave Mode prompt, duty/return-buffer rules, refundable booking
  // preference, and live travel data from Expedia Rapid, Amadeus, Travelpayouts, Booking.com, and Duffel.
  return NextResponse.json({ source: "mock", options: leaveModeOptions });
}
