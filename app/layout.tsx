import type { Metadata } from "next";
import Link from "next/link";
import "./globals.css";

export const metadata: Metadata = {
  title: "Mission Ready Vacations AI",
  description: "Family travel planned with military precision. AI-assisted planning for military and busy families."
};

const nav = [
  ["Planner", "/planner"], ["Leave Mode", "/leave-mode"], ["Results", "/results"],
  ["Compare", "/compare"], ["Packages", "/packages"], ["Pricing", "/pricing"]
];

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <header className="sticky top-0 z-50 border-b border-white/40 bg-sand/90 backdrop-blur">
          <div className="mx-auto flex max-w-7xl items-center justify-between gap-4 px-4 py-4 sm:px-6 lg:px-8">
            <Link href="/" className="flex items-center gap-3 font-black text-navy">
              <span className="grid h-10 w-10 place-items-center rounded-2xl bg-navy text-white">MR</span>
              <span className="leading-tight">Mission Ready<br className="sm:hidden" /> Vacations AI</span>
            </Link>
            <nav className="hidden items-center gap-5 text-sm font-semibold text-slate-700 md:flex">
              {nav.map(([label, href]) => <Link key={href} href={href} className="hover:text-mission">{label}</Link>)}
            </nav>
            <Link href="/planner" className="btn-primary hidden sm:inline-flex">Plan My Vacation</Link>
          </div>
        </header>
        <main>{children}</main>
        <footer className="border-t border-slate-200 bg-navy text-white">
          <div className="section grid gap-8 py-10 md:grid-cols-4">
            <div className="md:col-span-2">
              <h2 className="text-xl font-black">Mission Ready Vacations AI</h2>
              <p className="mt-3 max-w-xl text-sm text-slate-300">AI-assisted trip planning, cost comparison, and itinerary generation. Estimates only until confirmed by travel providers.</p>
            </div>
            <div className="grid gap-2 text-sm text-slate-300">
              <Link href="/about">About</Link><Link href="/saved-trips">Saved Trips</Link><Link href="/concierge">Concierge</Link><Link href="/admin">Admin</Link>
            </div>
            <div className="grid gap-2 text-sm text-slate-300">
              <Link href="/disclaimer">Travel Disclaimer</Link><Link href="/privacy">Privacy Policy</Link><Link href="/terms">Terms of Service</Link>
            </div>
          </div>
        </footer>
      </body>
    </html>
  );
}
