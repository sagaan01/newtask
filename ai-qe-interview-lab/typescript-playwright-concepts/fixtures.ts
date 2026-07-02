/**
 * CONCEPT FILE 5: typed custom fixtures - Playwright's dependency injection.
 * test.extend<T> takes a TYPE PARAMETER describing what we add; every test
 * destructures fully-typed, ready-to-use objects.
 */

import { test as base } from '@playwright/test';
import { ApiClient } from './src/api-client';
import { CheckoutPage } from './src/pages/CheckoutPage';

// CONCEPT: a type describing our custom fixtures - the contract between
// the framework and every test file.
type QEFixtures = {
  checkoutPage: CheckoutPage;
  api: ApiClient;
};

// CONCEPT: generic instantiation - test.extend<QEFixtures> makes
// `{ checkoutPage, api }` available and TYPED in every test signature.
export const test = base.extend<QEFixtures>({
  checkoutPage: async ({ page }, use) => {
    await use(new CheckoutPage(page));
  },
  api: async ({ request, baseURL }, use) => {
    // CONCEPT: non-null assertion (!) - baseURL is optional in Playwright's
    // types but our config always sets it; we assert that knowledge.
    await use(new ApiClient(request, baseURL!));
  },
});

export { expect } from '@playwright/test';
