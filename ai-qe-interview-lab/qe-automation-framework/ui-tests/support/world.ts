import { World, setWorldConstructor } from '@cucumber/cucumber';
import { BrowserContext, Page } from '@playwright/test';
import { CheckoutPage } from '../pages/CheckoutPage';

export class QEWorld extends World {
  context!: BrowserContext;
  page!: Page;
  checkoutPage!: CheckoutPage;
  baseUrl: string = process.env.BASE_URL ?? 'http://localhost:8787';
}

setWorldConstructor(QEWorld);
