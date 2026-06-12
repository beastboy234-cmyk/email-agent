# Mission Ready Vacations AI

**Family travel planned with military precision.**

Mission Ready Vacations AI is a production-ready MVP for an AI-assisted family travel planning platform. It helps military families and busy families compare practical vacation options based on estimated real cost, budget fit, kids, pets, refundability, travel time, hidden fees, family stress, and leave-mode risk.

> Compliance note: this app is not affiliated with the Department of Defense, DTS, DTMO, MWR, American Forces Travel, or any government agency. It does not directly sell flights, hotels, rental cars, cruises, or packages. Prices are estimates until confirmed by travel providers.

## Tech stack

- Next.js App Router
- TypeScript
- Tailwind CSS
- Supabase-ready SQL schema
- Mock travel data for MVP
- Placeholder API routes for AI, Stripe, PayPal, saved trips, concierge, and affiliate clicks
- Vercel-ready configuration

## Getting started

```bash
npm install
npm run dev
```

Open http://localhost:3000.

## Useful scripts

```bash
npm run dev
npm run lint
npm run build
npm run start
```

## Routes

- `/` landing page
- `/planner` family trip planner
- `/leave-mode` military Leave Mode planner
- `/results` AI trip results
- `/compare` trip comparison dashboard
- `/saved-trips` saved trips and family profile UI
- `/pricing` pricing page
- `/checkout` checkout placeholder
- `/concierge` concierge request flow
- `/admin` mock admin dashboard
- `/packages` destination packages
- `/about`, `/disclaimer`, `/privacy`, `/terms`

## API placeholders

- `POST /api/ai/generate-trip`
- `POST /api/ai/leave-mode`
- `GET|POST /api/payments/stripe`
- `GET|POST /api/payments/paypal`
- `POST /api/trips/save`
- `POST /api/concierge/request`
- `GET /api/affiliate/click`

The AI routes currently return mock trip data from `lib/mock-data.ts`. Comments in the routes show where future OpenAI and travel provider integrations should be connected.

## Connecting real APIs later

1. **OpenAI**: Replace the mock return in `/api/ai/generate-trip` and `/api/ai/leave-mode` with a server-side OpenAI Responses API call. Keep the structured form inputs and return a validated schema containing three options, Mission Ready Scores, estimated real costs, warnings, and rationale.
2. **Travel providers**: Add provider adapter modules for Expedia Rapid, Amadeus, Travelpayouts, Booking.com, and Duffel. Normalize provider prices into the Real Total Cost Calculator before scoring.
3. **Payments**: Replace checkout JSON placeholders with Stripe Checkout sessions and PayPal hosted checkout orders. Do not collect card data directly.
4. **Supabase**: Run `supabase/schema.sql`, then insert trip requests, trip results, saved trips, affiliate clicks, payments, and concierge requests from the API routes.
5. **Auth/admin**: Add Supabase Auth and protect `/admin` with role-based access.

## Supabase schema

Run `supabase/schema.sql` in your Supabase SQL editor or migration workflow. The schema includes:

- users
- family_profiles
- trip_requests
- trip_results
- saved_trips
- payments
- affiliate_clicks
- concierge_requests
- destination_packages
- admin_notes

## Vercel deployment

1. Push this repository to GitHub.
2. Import the project in Vercel.
3. Add environment variables from `.env.example`.
4. Deploy.
5. When real integrations are enabled, keep secrets server-side only.

## MVP limitations

- Uses mock travel data.
- Does not book travel.
- Does not process real payments.
- Does not authenticate users yet.
- Displays affiliate and booking links as placeholders.
