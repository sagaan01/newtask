import { test as base } from '@playwright/test';
import { LoginPage } from '../pages/login-page';
import { InventoryPage } from '../pages/inventory-page';
import { CartPage } from '../pages/cart-page';
import { CheckoutPage } from '../pages/checkout-page';

export const STANDARD_USER = 'standard_user';
export const LOCKED_OUT_USER = 'locked_out_user';
export const PASSWORD = 'secret_sauce';

type PomFixtures = {
  loginPage: LoginPage;
  inventoryPage: InventoryPage;
  cartPage: CartPage;
  checkoutPage: CheckoutPage;
  /** A page already logged in as the standard user, landed on the inventory page. */
  loggedInPage: InventoryPage;
};

/**
 * Custom fixtures wiring the page objects into every test, plus a
 * `loggedInPage` fixture that handles authentication as a precondition.
 */
export const test = base.extend<PomFixtures>({
  loginPage: async ({ page }, use) => {
    await use(new LoginPage(page));
  },
  inventoryPage: async ({ page }, use) => {
    await use(new InventoryPage(page));
  },
  cartPage: async ({ page }, use) => {
    await use(new CartPage(page));
  },
  checkoutPage: async ({ page }, use) => {
    await use(new CheckoutPage(page));
  },
  loggedInPage: async ({ loginPage, inventoryPage }, use) => {
    await loginPage.goto();
    await loginPage.login(STANDARD_USER, PASSWORD);
    await use(inventoryPage);
  },
});

export { expect } from '@playwright/test';
