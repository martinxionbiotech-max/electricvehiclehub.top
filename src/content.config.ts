import { defineCollection } from 'astro:content';
import { z } from 'astro/zod';
import { glob } from 'astro/loaders';

const blog = defineCollection({
  loader: glob({ pattern: '**/*.{md,mdx}', base: './src/content/blog' }),
  schema: z.object({
    title: z.string(),
    description: z.string(),
    publishedDate: z.coerce.date(),
    author: z.string(),
    image: z.string().optional(),
    tags: z.array(z.string()).default([]),
    draft: z.boolean().default(false),
  }),
});

const docs = defineCollection({
  loader: glob({ pattern: '**/*.{md,mdx}', base: './src/content/docs' }),
  schema: z.object({
    title: z.string(),
    description: z.string(),
    order: z.number().default(0),
    section: z.string(),
    draft: z.boolean().default(false),
  }),
});

const vehicles = defineCollection({
  loader: glob({ pattern: '**/*.{md,mdx}', base: './src/content/vehicles' }),
  schema: z.object({
    title: z.string(),
    description: z.string(),
    slug: z.string(),
    brand: z.string(),
    type: z.enum([
      'Sedan',
      'Hatchback',
      'SUV',
      'Crossover',
      'MPV',
      'Wagon',
      'Pickup',
      'Van',
      'Coupe',
      'Convertible',
      'Sports Car',
      'Other',
      'Unknown',
    ]),
    powertrain: z.enum(['BEV', 'PHEV', 'EREV', 'HEV', 'ICE', 'FCEV', 'Unknown']),
    price_usd: z.number(),
    // Five strictly-separated price bases (P3 rule #4). Never conflate ex-factory
    // with MSRP, market reference, FOB, or landed cost. Default reflects the
    // documented source basis (China ex-factory catalog/manufacturer starting price).
    price_type: z
      .enum([
        'Official MSRP',
        'China market reference price',
        'China ex-factory reference price',
        'FOB quotation',
        'Landed cost estimate',
        'Reference (unverified)',
      ])
      .default('China ex-factory reference price'),
    currency: z.string().default('USD'),
    model_year: z.number().nullable().optional(),
    range_cltc_km: z.number().nullable().optional(),
    range_epa_km: z.number().nullable().optional(),
    range_nedc_km: z.number().nullable().optional(),
    range_long_km: z.number().nullable().optional(),
    battery_kwh: z.number().nullable().optional(),
    motor_power_kw: z.number().nullable().optional(),
    torque_nm: z.number().nullable().optional(),
    accel_0_100_s: z.number().nullable().optional(),
    top_speed_kmh: z.number().nullable().optional(),
    length_mm: z.number().nullable().optional(),
    width_mm: z.number().nullable().optional(),
    height_mm: z.number().nullable().optional(),
    wheelbase_mm: z.number().nullable().optional(),
    weight_kg: z.number().nullable().optional(),
    efficiency_kwh_100km: z.number().nullable().optional(),
    fast_charge: z.string().nullable().default(null),
    landed_cost: z.any().optional(),
    landed_cost_markets: z.any().default([]),
    image: z.string().optional(),
    image_credit: z.string().optional(),
    image_source: z.string().optional(),
    publishedDate: z.coerce.date(),
    author: z.string(),
    tags: z.array(z.string()).default([]),
    data_tier: z.number().optional(),
    data_source: z.string().optional(),
    data_updated: z.string().optional(),
    data_reviewed: z.boolean().optional(),
    verification_status: z.string().optional(),
    quality_tier: z.string().optional(),
    confidence: z.string().optional(),
    family: z.string().optional(),
    // ── Parameter-level source metadata (verification-system, batch 01) ──
    // Five-tuple per key parameter (price / range / battery / motor / accel /
    // charge) + a three-state status. Conflict values are flagged, never
    // auto-filled. Canonical batch data lives in src/data/parameter-verification.json;
    // this field documents the frontmatter path for future hand-fixed records.
    param_verification: z
      .record(
        z.object({
          source: z.string(),
          verified_at: z.string().optional(),
          model_year: z.number().nullable().optional(),
          trim: z.string().optional(),
          confidence: z.enum(['high', 'medium', 'low']).optional(),
          status: z.enum(['verified', 'mismatch', 'unverifiable', 'conflict']).optional(),
          test_standard: z.enum(['CLTC', 'WLTP', 'EPA', 'NEDC']).optional(),
          note: z.string().optional(),
        }),
      )
      .optional(),
    // ── China EV Mart deep-profile fields (five-section template; all optional) ──
    // ① Entity Snapshot
    trim: z.string().optional(),
    range_wltp_km: z.number().nullable().optional(),
    fob_price_usd_min: z.number().nullable().optional(),
    fob_price_usd_max: z.number().nullable().optional(),
    // ② Powertrain & Architecture
    battery_type: z.string().optional(),
    drive_type: z.string().optional(),
    motor_type: z.string().optional(),
    motor_model: z.string().optional(),
    total_power_kw: z.number().nullable().optional(),
    battery_thermal: z.string().optional(),
    heat_pump: z.string().optional(),
    suspension_front: z.string().optional(),
    suspension_rear: z.string().optional(),
    brakes: z.string().optional(),
    drag_coefficient: z.number().nullable().optional(),
    // ③ Dimensions & Logistics
    gross_weight_kg: z.number().nullable().optional(),
    ground_clearance_mm: z.number().nullable().optional(),
    trunk_l: z.number().nullable().optional(),
    // ④ Market Compliance & Export Profile
    charging_interface: z.string().optional(),
    charging_adapter: z.string().optional(),
    infotainment_language: z.string().optional(),
    network_bands: z.string().optional(),
    certification_notes: z.string().optional(),
    hs_code: z.string().optional(),
  }),
});

const brands = defineCollection({
  loader: glob({ pattern: "**/*.{md,mdx}", base: "./src/content/brands" }),
  schema: z.object({
    title: z.string(),
    description: z.string(),
    brand_name: z.string(),
    established: z.string(),
    parent_manufacturer: z.string(),
    parent_location: z.string(),
    parent_founded: z.string(),
    website: z.string(),
    model_count: z.number(),
    publishedDate: z.coerce.date(),
    tags: z.array(z.string()).default([]),
  }),
});

export const collections = { blog, docs, vehicles, brands };
