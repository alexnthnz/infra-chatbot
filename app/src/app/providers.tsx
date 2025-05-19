'use client';

import { ReactNode } from 'react';
import { Provider } from 'jotai';
import { Toaster } from '@/components/ui/sonner';

export function Providers({ children }: { children: ReactNode }) {
  return (
    <Provider>
      {children}
      <Toaster />
    </Provider>
  );
}
