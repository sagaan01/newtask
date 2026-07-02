/**
 * CONCEPT FILE 2: generics in practice.
 * One client class, typed responses for every endpoint - no `any`, no casts
 * scattered through tests.
 */

import { APIRequestContext } from '@playwright/test';
import { ApiResponse } from './types';

export class ApiClient {
  // CONCEPT: parameter properties + access modifiers - `private readonly`
  // declares and assigns fields in one line; nothing outside can touch them.
  constructor(
    private readonly request: APIRequestContext,
    private readonly baseUrl: string,
  ) {}

  // CONCEPT: generic method - the CALLER declares what type the response
  // body has: api.get<Order>(...) returns Promise<ApiResponse<Order>>.
  // CONCEPT: async/await returning Promise<T>.
  async get<T>(path: string): Promise<ApiResponse<T>> {
    const resp = await this.request.get(`${this.baseUrl}${path}`);
    return { status: resp.status(), body: (await resp.json()) as T };
  }

  // CONCEPT: `unknown` for the payload - safer than `any`. The client
  // doesn't care what goes out, but callers get full typing on what comes back.
  async post<T>(path: string, payload: unknown): Promise<ApiResponse<T>> {
    const resp = await this.request.post(`${this.baseUrl}${path}`, { data: payload });
    return { status: resp.status(), body: (await resp.json()) as T };
  }
}
