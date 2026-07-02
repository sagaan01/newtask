import { test, expect } from '@playwright/test';

const TODO_ITEMS = ['buy some cheese', 'feed the cat', 'book a doctors appointment'];

test.describe('TodoMVC', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('https://demo.playwright.dev/todomvc/');
  });

  test('adds todo items', async ({ page }) => {
    const newTodo = page.getByPlaceholder('What needs to be done?');

    for (const item of TODO_ITEMS) {
      await newTodo.fill(item);
      await newTodo.press('Enter');
    }

    await expect(page.getByTestId('todo-title')).toHaveText(TODO_ITEMS);
    await expect(page.getByTestId('todo-count')).toContainText('3');
  });

  test('marks an item as completed', async ({ page }) => {
    const newTodo = page.getByPlaceholder('What needs to be done?');
    await newTodo.fill(TODO_ITEMS[0]);
    await newTodo.press('Enter');

    await page.getByRole('checkbox', { name: 'Toggle Todo' }).check();

    await expect(page.getByTestId('todo-item')).toHaveClass('completed');
    await expect(page.getByTestId('todo-count')).toContainText('0');
  });

  test('filters active and completed items', async ({ page }) => {
    const newTodo = page.getByPlaceholder('What needs to be done?');
    for (const item of TODO_ITEMS.slice(0, 2)) {
      await newTodo.fill(item);
      await newTodo.press('Enter');
    }
    await page.getByTestId('todo-item').first().getByRole('checkbox').check();

    await page.getByRole('link', { name: 'Active' }).click();
    await expect(page.getByTestId('todo-title')).toHaveText([TODO_ITEMS[1]]);

    await page.getByRole('link', { name: 'Completed' }).click();
    await expect(page.getByTestId('todo-title')).toHaveText([TODO_ITEMS[0]]);
  });

  test('clears completed items', async ({ page }) => {
    const newTodo = page.getByPlaceholder('What needs to be done?');
    for (const item of TODO_ITEMS.slice(0, 2)) {
      await newTodo.fill(item);
      await newTodo.press('Enter');
    }
    await page.getByTestId('todo-item').first().getByRole('checkbox').check();

    await page.getByRole('button', { name: 'Clear completed' }).click();

    await expect(page.getByTestId('todo-title')).toHaveText([TODO_ITEMS[1]]);
  });

  test('persists todos across page reloads', async ({ page }) => {
    const newTodo = page.getByPlaceholder('What needs to be done?');
    await newTodo.fill(TODO_ITEMS[0]);
    await newTodo.press('Enter');

    await page.reload();

    await expect(page.getByTestId('todo-title')).toHaveText([TODO_ITEMS[0]]);
  });
});
