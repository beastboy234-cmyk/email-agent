import { NextResponse } from "next/server";
export async function GET() { return NextResponse.json({ provider: "Stripe", status: "placeholder", note: "Future integration creates a Stripe Checkout hosted session. Do not collect cards directly." }); }
export async function POST() { return GET(); }
