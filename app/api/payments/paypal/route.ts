import { NextResponse } from "next/server";
export async function GET() { return NextResponse.json({ provider: "PayPal", status: "placeholder", note: "Future integration creates a PayPal hosted checkout order. Do not collect cards directly." }); }
export async function POST() { return GET(); }
