declare module 'vitest';
declare module '@testing-library/react';
declare module '@testing-library/jest-dom';

// Add axios error type
declare namespace Axios {
  interface AxiosError<T = any> {
    response?: {
      data?: T;
      status?: number;
      headers?: Record<string, string>;
    };
  }
}