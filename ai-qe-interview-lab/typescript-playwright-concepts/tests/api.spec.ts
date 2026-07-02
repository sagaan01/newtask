/**
 * API tests: generics, type guards, builders with Partial<T>,
 * and compile-time contract checking.
 */

import { expect, test } from '../fixtures';
import {
  ApiError,
  Order,
  OrderStatus,
  buildOrderPayload,
  isApiError,
} from '../src/types';

test.describe('Orders API', () => {
  test('creates an order with the full typed contract', async ({ api }) => {
    // CONCEPT: generic call site - api.post<Order> means `body` below is an
    // Order. Accessing body.stauts (typo) would fail compilation.
    const { status, body } = await api.post<Order>('/api/orders', buildOrderPayload());

    expect(status).toBe(201);
    expect(body.id).toBeTruthy();
    expect(body.total).toBe(49.99);

    // CONCEPT: union type as an executable contract - this assertion list
    // is derived from OrderStatus; a new status in the API forces a
    // conscious update here.
    const validStatuses: OrderStatus[] = ['CREATED', 'PAID', 'REFUNDED'];
    expect(validStatuses).toContain(body.status);
  });

  test('rejects order with missing email', async ({ api }) => {
    // CONCEPT: builder + Partial - the test declares ONLY the deviation
    // that matters (email removed), keeping intent obvious.
    const { email: _omitted, ...noEmail } = buildOrderPayload();
    const { status, body } = await api.post<ApiError>('/api/orders', noEmail);

    expect(status).toBe(400);

    // CONCEPT: type guard narrowing - before the guard, body could be
    // anything; after it, TypeScript KNOWS body.error is a string.
    expect(isApiError(body)).toBe(true);
    if (isApiError(body)) {
      expect(body.error).toContain('email');
    }
  });

  test('rejects non-positive totals', async ({ api }) => {
    const { status } = await api.post<ApiError>(
      '/api/orders',
      buildOrderPayload({ total: -10 }), // override just one field
    );
    expect(status).toBe(400);
  });

  test('unknown order returns typed error', async ({ api }) => {
    const { status, body } = await api.get<ApiError>('/api/orders/nope123');
    expect(status).toBe(404);
    expect(isApiError(body)).toBe(true);
  });
});
