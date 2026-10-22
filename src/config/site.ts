/**
 * Site Configuration — China EV Mart
 *
 * @description
 * China EV Mart: an independent information platform for discovering Chinese
 * new-energy vehicles, comparing specifications, researching automotive
 * technology, and evaluating export-market requirements.
 * Company: Chengguang Energy (Jinzhou Chengguang Power Source Co., Ltd.)
 * Author: Wei Wang, EV & Battery Industry Analyst
 * Primary contact: info@electricvehiclehub.top (business email)
 */

import type { SocialLinks, LegalConfig } from '../lib/types';

/** Site name displayed in header, footer, and meta tags */
export const name = import.meta.env.SITE_NAME || 'China EV Mart';

/** Site description for SEO and meta tags */
export const description =
  import.meta.env.SITE_DESCRIPTION ||
  'An independent information platform for discovering Chinese new-energy vehicles, comparing vehicle specifications, researching automotive technology, and evaluating export-market requirements.';

/** Production URL of your site (used for sitemap, RSS, canonical URLs) */
export const url = import.meta.env.SITE_URL || 'https://chinaevmart.com';

/** Author name for meta tags and copyright */
export const author = import.meta.env.SITE_AUTHOR || 'Wei Wang';

/** Path to logo file (relative to /public) */
export const logo = '/logo.svg';

/** Path to Open Graph image (relative to /public) */
export const ogImage = '/images/og-image.png';

/** Social media links */
export const social: SocialLinks = {
  twitter: 'https://x.com/cnevhub',
  github: 'https://github.com/martinxionbiotech-max/CNEVhub',
  discord: '',
};

/** Company (EEAT Organization) */
export const company = {
  name: 'Chengguang Energy',
  legalName: 'Jinzhou Chengguang Power Source Co., Ltd.',
  description:
    'Chengguang Energy (Jinzhou Chengguang Power Source Co., Ltd.) is an automotive battery manufacturer founded in 2002 whose quality management system is certified to IATF 16949, publishing an independent product database of Chinese EV specifications, versions, and technology data.',
  url: 'https://chinaevmart.com',
  logo: '/logo.svg',
  email: 'info@electricvehiclehub.top',
  author: 'Wei Wang',
  authorRole: 'EV & Battery Industry Analyst',
  authorBio:
    'Wei Wang has spent many years in automotive battery production, and in recent years has focused on commercial research into electric vehicles — import economics, tariffs, and cross-border compliance.',
};

/** Legal configuration for privacy policy and terms pages */
export const legal: LegalConfig = {
  privacyEmail: 'privacy@electricvehiclehub.top',
  legalEmail: 'legal@electricvehiclehub.top',
  lastUpdated: 'September 5, 2026',
};
