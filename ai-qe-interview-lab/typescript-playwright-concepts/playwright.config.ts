// CONCEPT: typed configuration - defineConfig gives autocomplete and
// compile-time validation of every option. A typo like `retrys` fails
// the build instead of being silently ignored at runtime.
import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: './tests',
  fullyParallel: true,
  retries: 0,
  reporter: [['list']],
  use: {
    baseURL: 'http://localhost:8790',
    trace: 'retain-on-failure',
    testIdAttribute: 'data-testid',
  },
  // Auto-start the app under test (reuses Mini Shop from Category 2)
  webServer: {
    command: 'python3 ../qe-automation-framework/app/server.py --port 8790',
    url: 'http://localhost:8790/health',
    reuseExistingServer: true,
    timeout: 15_000,
  },
});
