import { Given, Then, When } from '@cucumber/cucumber';
import { QEWorld } from '../support/world';

Given('I am on the checkout page', async function (this: QEWorld) {
  await this.checkoutPage.open(this.baseUrl);
});

When('I enter email {string}', async function (this: QEWorld, email: string) {
  await this.checkoutPage.enterEmail(email);
});

When('I click Pay Now', async function (this: QEWorld) {
  await this.checkoutPage.clickPayNow();
});

Then('I should see the order confirmation', async function (this: QEWorld) {
  await this.checkoutPage.expectConfirmation();
});

Then('I should see the error {string}', async function (this: QEWorld, message: string) {
  await this.checkoutPage.expectError(message);
});

Then('the cart total should be {string}', async function (this: QEWorld, total: string) {
  await this.checkoutPage.expectCartTotal(total);
});
