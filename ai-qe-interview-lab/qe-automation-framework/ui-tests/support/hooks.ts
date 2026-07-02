import { After, AfterAll, Before, BeforeAll, Status, setDefaultTimeout } from '@cucumber/cucumber';
import { Browser, chromium } from '@playwright/test';
import { CheckoutPage } from '../pages/CheckoutPage';
import { QEWorld } from './world';

setDefaultTimeout(30_000);

let browser: Browser;

BeforeAll(async () => {
  browser = await chromium.launch({ headless: true });
});

Before(async function (this: QEWorld) {
  this.context = await browser.newContext();
  this.page = await this.context.newPage();
  this.checkoutPage = new CheckoutPage(this.page);
});

After(async function (this: QEWorld, { result, pickle }) {
  if (result?.status === Status.FAILED) {
    await this.page.screenshot({
      path: `reports/screenshots/${pickle.name.replace(/\s+/g, '_')}.png`,
    });
  }
  await this.context.close();
});

AfterAll(async () => {
  await browser.close();
});
