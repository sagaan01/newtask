import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

test.describe('Accessibility scans (axe-core)', () => {
  test('TodoMVC has no critical accessibility violations', async ({ page }) => {
    await page.goto('https://demo.playwright.dev/todomvc/');

    const results = await new AxeBuilder({ page }).analyze();

    const critical = results.violations.filter((v) => v.impact === 'critical');
    expect(critical, JSON.stringify(critical, null, 2)).toEqual([]);
  });

  test('SauceDemo login page has no critical accessibility violations', async ({ page }) => {
    await page.goto('https://www.saucedemo.com/');

    const results = await new AxeBuilder({ page })
      .withTags(['wcag2a', 'wcag2aa'])
      .analyze();

    const critical = results.violations.filter((v) => v.impact === 'critical');
    expect(critical, JSON.stringify(critical, null, 2)).toEqual([]);
  });
});
