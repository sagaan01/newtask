/**
 * CONCEPT FILE 1: the type system.
 * Interfaces, type aliases, union types, literal types, const assertions,
 * utility types, and type guards - all modeling the API we test.
 */

// CONCEPT: interface - describes the exact shape of an API response.
// If the API contract changes, every test touching Order fails to COMPILE.
export interface Order {
  id: string;
  email: string;
  total: number;
  status: OrderStatus;
}

// CONCEPT: union of string literals - OrderStatus can ONLY be one of these.
// `order.status === 'CREATTED'` (typo) is a compile error, not a flaky test.
export type OrderStatus = 'CREATED' | 'PAID' | 'REFUNDED';

// CONCEPT: type alias for a request payload, kept separate from the
// response type because requests have no id/status yet.
export type OrderPayload = {
  email: string;
  total: number;
};

// CONCEPT: const assertion (`as const`) - a modern alternative to enum.
// Routes is deeply readonly; Route becomes the union '/' | '/health'.
export const Routes = {
  checkout: '/',
  health: '/health',
} as const;
export type Route = (typeof Routes)[keyof typeof Routes];

// CONCEPT: interface for the API's error shape.
export interface ApiError {
  error: string;
}

// CONCEPT: type guard - runtime check that NARROWS the static type.
// After `if (isApiError(body))`, TypeScript knows body.error exists.
export function isApiError(body: unknown): body is ApiError {
  return (
    typeof body === 'object' &&
    body !== null &&
    typeof (body as Record<string, unknown>).error === 'string'
  );
}

// CONCEPT: utility type Partial<T> + default parameter = test data builder.
// Tests state ONLY what matters for the scenario; the builder fills the rest.
export function buildOrderPayload(overrides: Partial<OrderPayload> = {}): OrderPayload {
  return {
    email: 'ts-demo@example.com',
    total: 49.99,
    ...overrides,
  };
}

// CONCEPT: generic type - a reusable "typed envelope" for any API response.
// One shape serves Order, ApiError, health checks - anything.
export type ApiResponse<T> = {
  status: number;
  body: T;
};
