/**
 * UI tests: typed fixtures, Page Object inheritance, and
 * typed data-driven testing.
 */

import { expect, test } from '../fixtures';

test.describe('Checkout UI', () => {
  test('successful checkout shows confirmation', async ({ checkoutPage }) => {
    await checkoutPage.open(); // inherited from BasePage
    await checkoutPage.submitCheckout('ui-demo@example.com');
    await checkoutPage.expectOrderConfirmed();
  });

  test('missing email shows validation error', async ({ checkoutPage }) => {
    await checkoutPage.open();
    await checkoutPage.submitCheckout(); // optional param default: ''
    await checkoutPage.expectValidationError('Email is required');
  });

  // CONCEPT: typed data-driven tests - the array's inline type means a
  // malformed row (missing field, wrong type) is a compile error, and
  // each row generates an independently-reported test.
  const invalidEmails: { label: string; email: string }[] = [
    { label: 'spaces only', email: '   ' },
    { label: 'empty string', email: '' },
  ];

  for (const { label, email } of invalidEmails) {
    test(`rejects invalid email: ${label}`, async ({ checkoutPage }) => {
      await checkoutPage.open();
      await checkoutPage.submitCheckout(email.trim());
      await checkoutPage.expectValidationError('Email is required');
    });
  }
});

test('UI order is retrievable via API afterwards', async ({ checkoutPage, api, page }) => {
  // CONCEPT: composing fixtures - one test uses UI AND API layers together.
  await checkoutPage.open();
  await checkoutPage.submitCheckout('hybrid@example.com');
  await checkoutPage.expectOrderConfirmed();

  const orderId = await page.getByTestId('order-id').textContent();
  const { status, body } = await api.get<import('../src/types').Order>(`/api/orders/${orderId}`);

  expect(status).toBe(200);
  expect(body.email).toBe('hybrid@example.com'); // body is typed as Order
  expect(body.status).toBe('CREATED');
});
