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
  email: 'info@electricvehiclehub.top',
  supportEmail: 'info@electricvehiclehub.top',
  salesEmail: 'info@electricvehiclehub.top',
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
    value: 'info@electricvehiclehub.top',
    href: 'mailto:info@electricvehiclehub.top',
  },
];

/** FAQ items displayed on the contact page */
export const contactFAQs: ContactFAQ[] = [
  {
    question: "What's your typical response time?",
    answer: 'We respond to most inquiries within 24 hours on business days (GMT+8).',
  },
  {
    question: 'Can you help me source a specific Chinese EV?',
    answer:
      'Yes. Send us the model and destination country, and we will provide a transparent landed-cost breakdown including duties, countervailing tariffs, VAT, freight, and certification.',
  },
  {
    question: 'Do you sell vehicles directly?',
    answer:
      'No. China EV Mart is an independent information platform. We provide landed-cost intelligence and sourcing guidance, but do not sell vehicles or act on behalf of any manufacturer.',
  },
];

