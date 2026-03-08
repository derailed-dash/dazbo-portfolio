import '@testing-library/jest-dom';
import { vi } from 'vitest';

// Fix relative URL issues in JSDOM by mocking fetch
if (typeof globalThis.fetch === 'undefined' || (globalThis.fetch as any)._isMock) {
  globalThis.fetch = vi.fn().mockImplementation(() => 
    Promise.resolve({
      ok: false,
      status: 404,
      json: async () => ({}),
    })
  );
  (globalThis.fetch as any)._isMock = true;
}
