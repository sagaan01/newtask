import { test, expect } from '@playwright/test';

test.describe('Network interception and mocking', () => {
  test('mocks an API response with route.fulfill', async ({ page }) => {
    await page.route('**/api/products', (route) =>
      route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({ products: [{ id: 999, title: 'Mocked Product' }] }),
      })
    );

    await page.goto('https://demo.playwright.dev/todomvc/');
    const data = await page.evaluate(async () => {
      const res = await fetch('/api/products');
      return res.json();
    });

    expect(data.products[0].title).toBe('Mocked Product');
  });

  test('serves a fully mocked page with route.fulfill', async ({ page }) => {
    await page.route('**/mocked-page', (route) =>
      route.fulfill({
        status: 200,
        contentType: 'text/html',
        body: '<h1>Mocked by Playwright</h1><button id="cta">Click me</button>',
      })
    );

    await page.goto('https://example.com/mocked-page');

    await expect(page.getByRole('heading', { name: 'Mocked by Playwright' })).toBeVisible();
    await expect(page.locator('#cta')).toBeEnabled();
  });

  test('blocks font and analytics requests with route.abort and the page still works', async ({
    page,
  }) => {
    const blockedUrls: string[] = [];
    await page.route('**/*', (route) => {
      const request = route.request();
      if (request.resourceType() === 'font' || request.url().includes('backtrace.io')) {
        blockedUrls.push(request.url());
        return route.abort();
      }
      return route.continue();
    });

    await page.goto('https://www.saucedemo.com/');

    await expect(page.locator('[data-test="login-button"]')).toBeVisible();
    expect(blockedUrls.length).toBeGreaterThan(0);
  });

  test('records requests made by the page', async ({ page }) => {
    const requests: string[] = [];
    page.on('request', (request) => requests.push(request.url()));

    await page.goto('https://demo.playwright.dev/todomvc/');

    expect(requests.some((url) => url.includes('todomvc'))).toBeTruthy();
  });
});
