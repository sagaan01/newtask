/**
 * CONCEPT FILE 3: OOP for Page Objects.
 * Abstract classes, inheritance, protected members, readonly fields.
 */

import { Locator, Page } from '@playwright/test';
import { Route } from '../types';

// CONCEPT: abstract class - cannot be instantiated directly; it exists to
// share behavior and FORCE subclasses to define their own `path`.
export abstract class BasePage {
  // CONCEPT: `protected readonly` - subclasses can use `this.page`,
  // tests cannot reach around the Page Object, and nobody can reassign it.
  protected constructor(protected readonly page: Page) {}

  // CONCEPT: abstract member - every concrete page MUST declare its route,
  // and the Route union type means only known routes compile.
  abstract readonly path: Route;

  // CONCEPT: shared behavior inherited by every page - write `open()` once.
  async open(): Promise<void> {
    await this.page.goto(this.path);
  }

  // CONCEPT: protected helper + return type annotation - a single place
  // defining HOW this framework locates elements (testId strategy).
  protected byTestId(id: string): Locator {
    return this.page.getByTestId(id);
  }
}
