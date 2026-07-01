import { Page, expect } from '@playwright/test';

/**
 * Page Object: all locators and UI actions for the checkout page live here.
 * Step definitions never touch selectors directly.
 */
export class CheckoutPage {
  constructor(private page: Page) {}

  private emailInput = () => this.page.getByTestId('email-input');
  private payNowButton = () => this.page.getByTestId('pay-now');
  private emailError = () => this.page.getByTestId('email-error');
  private confirmation = () => this.page.getByTestId('order-confirmation');
  private cartTotal = () => this.page.getByTestId('cart-total');

  async open(baseUrl: string): Promise<void> {
    await this.page.goto(baseUrl);
  }

  async enterEmail(email: string): Promise<void> {
    await this.emailInput().fill(email);
  }

  async clickPayNow(): Promise<void> {
    await this.payNowButton().click();
  }

  async expectConfirmation(): Promise<void> {
    await expect(this.confirmation()).toBeVisible();
    await expect(this.page.getByTestId('order-id')).not.toBeEmpty();
  }

  async expectError(message: string): Promise<void> {
    await expect(this.emailError()).toBeVisible();
    await expect(this.emailError()).toHaveText(message);
  }

  async expectCartTotal(total: string): Promise<void> {
    await expect(this.cartTotal()).toHaveText(total);
  }
}
