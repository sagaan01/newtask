/**
 * CONCEPT FILE 4: a concrete Page Object - inheritance in action.
 */

import { Page, expect } from '@playwright/test';
import { Routes } from '../types';
import { BasePage } from './BasePage';

// CONCEPT: `extends` - CheckoutPage inherits open() and byTestId() from
// BasePage and is FORCED by the compiler to provide `path`.
export class CheckoutPage extends BasePage {
  readonly path = Routes.checkout;

  constructor(page: Page) {
    super(page); // CONCEPT: super() call required by inheritance
  }

  // CONCEPT: private locator factories - selectors are implementation
  // details; tests can only call the public, business-named methods below.
  private emailInput = () => this.byTestId('email-input');
  private payNowButton = () => this.byTestId('pay-now');
  private confirmation = () => this.byTestId('order-confirmation');
  private emailError = () => this.byTestId('email-error');

  // CONCEPT: optional parameter with default - callers may omit the email
  // to test the empty case, mirroring buildOrderPayload's Partial pattern.
  async submitCheckout(email = ''): Promise<void> {
    if (email) {
      await this.emailInput().fill(email);
    }
    await this.payNowButton().click();
  }

  async expectOrderConfirmed(): Promise<void> {
    await expect(this.confirmation()).toBeVisible();
    await expect(this.byTestId('order-id')).not.toBeEmpty();
  }

  async expectValidationError(message: string): Promise<void> {
    await expect(this.emailError()).toHaveText(message);
  }
}
