/**
 * Contact Page Configuration — China EV Mart
 *
 * Real company + author contact information for EEAT.
 * Company: Chengguang Energy (Jinzhou Chengguang Power Source Co., Ltd.)
 * Author: Wei Wang, EV & Battery Industry Analyst
 * Primary contact: Aaron.W
 */

import type { ContactInfo, ContactMethod, ContactFAQ } from '../lib/types';

/** Contact information used across contact page and legal pages */
export const contact: ContactInfo = {
  email: 'info@chinaevmart.com',
  supportEmail: 'info@chinaevmart.com',
  salesEmail: 'info@chinaevmart.com',
  address: {
    street: '',
    city: 'Jinzhou',
    state: 'Hebei',
    zip: '',
    country: 'China',
  },
};

/** Contact methods displayed on the contact page */
export const contactMethods: ContactMethod[] = [
  {
    icon: 'lucide:mail',
    label: 'Email',
    value: 'info@chinaevmart.com',
    href: 'mailto:info@chinaevmart.com',
  },
];

/** FAQ items displayed on the contact page */
export const contactFAQs: ContactFAQ[] = [
  {
    question: "What's your typical response time?",
    answer: 'We respond to most inquiries within 24 hours on business days (GMT+8).',
  },
  {
    question: "Can you help me source a specific Chinese EV?",
    answer:
      'We can offer specification guidance for a specific model — clarify the product record, its battery, powertrain, and price basis. For export guidance on a specific model, quantity, and destination, use the request form on the [export guidance page](/quote/). We do not act as a purchasing agent or broker, and we do not provide transactional prices or quotes.',
  },
  {
    question: 'Do you sell vehicles directly?',
    answer:
      'No. China EV Mart is an independent information platform. We catalog and clarify Chinese EV product data, but we do not sell vehicles, source vehicles, or act on behalf of any manufacturer.',
  },
  {
    question: 'Does China EV Mart speak for vehicle manufacturers?',
    answer:
      'No. Our records and analysis do not represent the official position of any manufacturer, brand, or government authority. Manufacturer specifications are attributed to the manufacturer, not stated as our own finding. For landed-cost figures, see the methodology on electricvehiclehub.net.',
  },
];

