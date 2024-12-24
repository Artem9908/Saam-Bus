import '@testing-library/jest-dom';
import { expect, afterEach, beforeAll, afterAll, vi } from 'vitest';
import { cleanup } from '@testing-library/react';
import * as matchers from '@testing-library/jest-dom/matchers';

// Extend Vitest's expect with Jest DOM matchers
expect.extend(matchers as any);

// Cleanup after each test
afterEach(() => {
  cleanup();
});

beforeAll(() => {
  // Mock window.open
  vi.spyOn(window, 'open').mockImplementation(() => null);
});

afterAll(() => {
  vi.restoreAllMocks();
}); 