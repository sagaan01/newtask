import { test, expect, STANDARD_USER, LOCKED_OUT_USER, PASSWORD } from '../../fixtures/pom-fixtures';

test.describe('SauceDemo shopping flows (Page Object Model)', () => {
  test('logs in with valid credentials', async ({ loginPage, inventoryPage }) => {
    await loginPage.goto();
    await loginPage.login(STANDARD_USER, PASSWORD);

    await expect(inventoryPage.title).toHaveText('Products');
    await expect(inventoryPage.inventoryItems).toHaveCount(6);
  });

  test('shows an error for a locked out user', async ({ loginPage }) => {
    await loginPage.goto();
    await loginPage.login(LOCKED_OUT_USER, PASSWORD);

    await expect(loginPage.errorMessage).toContainText('Sorry, this user has been locked out');
  });

  test('shows an error for invalid credentials', async ({ loginPage }) => {
    await loginPage.goto();
    await loginPage.login('invalid_user', 'wrong_password');

    await expect(loginPage.errorMessage).toContainText(
      'Username and password do not match any user in this service'
    );
  });

  test('sorts products by price low to high', async ({ loggedInPage }) => {
    await loggedInPage.sortBy('lohi');

    const prices = await loggedInPage.getPrices();
    const sorted = [...prices].sort((a, b) => a - b);
    expect(prices).toEqual(sorted);
  });

  test('completes a full purchase (add to cart, checkout, finish)', async ({
    loggedInPage,
    cartPage,
    checkoutPage,
  }) => {
    await loggedInPage.addItemToCart('Sauce Labs Backpack');
    await loggedInPage.addItemToCart('Sauce Labs Bike Light');
    await expect(loggedInPage.cartBadge).toHaveText('2');

    await loggedInPage.openCart();
    await expect(cartPage.cartItems).toHaveCount(2);
    await cartPage.checkout();

    await checkoutPage.fillInformation('Quality', 'Engineer', '12345');
    await expect(checkoutPage.summaryTotal).toContainText('Total');
    await checkoutPage.finish();

    await expect(checkoutPage.completeHeader).toHaveText('Thank you for your order!');
  });
});
