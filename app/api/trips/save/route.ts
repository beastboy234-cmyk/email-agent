import { NextResponse } from "next/server";
export async function POST() { return NextResponse.json({ status: "saved_placeholder", note: "Future Supabase insert into saved_trips." }); }
