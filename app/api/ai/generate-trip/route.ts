import { NextResponse } from "next/server";
import { tripOptions } from "@/lib/mock-data";

export async function POST() {
  // Future OpenAI integration: validate structured planner input, enrich with policy-aware prompts,
  // call OpenAI Responses API, and merge with live provider data from Expedia Rapid, Amadeus,
  // Travelpayouts, Booking.com, and Duffel before returning scored options.
  return NextResponse.json({ source: "mock", options: tripOptions });
}
