import { test, expect } from '@playwright/test';

const BASE_URL = 'https://dummyjson.com';

test.describe('DummyJSON API', () => {
  test('GET a single product returns the expected schema', async ({ request }) => {
    const response = await request.get(`${BASE_URL}/products/1`);

    expect(response.status()).toBe(200);
    const product = await response.json();
    expect(product).toMatchObject({
      id: 1,
      title: expect.any(String),
      price: expect.any(Number),
      category: expect.any(String),
    });
  });

  test('GET products supports pagination via limit and skip', async ({ request }) => {
    const response = await request.get(`${BASE_URL}/products`, {
      params: { limit: 5, skip: 10 },
    });

    expect(response.ok()).toBeTruthy();
    const body = await response.json();
    expect(body.products).toHaveLength(5);
    expect(body.skip).toBe(10);
    expect(body.products[0].id).toBe(11);
  });

  test('GET search filters products by query', async ({ request }) => {
    const response = await request.get(`${BASE_URL}/products/search`, {
      params: { q: 'phone' },
    });

    expect(response.ok()).toBeTruthy();
    const body = await response.json();
    expect(body.total).toBeGreaterThan(0);
    for (const product of body.products) {
      const haystack = JSON.stringify(product).toLowerCase();
      expect(haystack).toContain('phone');
    }
  });

  test('POST creates a new product', async ({ request }) => {
    const response = await request.post(`${BASE_URL}/products/add`, {
      data: { title: 'Test Automation Handbook', price: 42 },
    });

    expect(response.status()).toBe(201);
    const created = await response.json();
    expect(created.title).toBe('Test Automation Handbook');
    expect(created.id).toEqual(expect.any(Number));
  });

  test('PUT updates an existing product', async ({ request }) => {
    const response = await request.put(`${BASE_URL}/products/1`, {
      data: { title: 'Updated Product Title' },
    });

    expect(response.ok()).toBeTruthy();
    const updated = await response.json();
    expect(updated.id).toBe(1);
    expect(updated.title).toBe('Updated Product Title');
  });

  test('GET a missing product returns 404', async ({ request }) => {
    const response = await request.get(`${BASE_URL}/products/0`);

    expect(response.status()).toBe(404);
  });
});
