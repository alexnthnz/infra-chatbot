'use client';

import { ArrowRightOnRectangleIcon } from '@heroicons/react/24/outline';
import { signOut } from 'next-auth/react';
import { Button } from '@/components/ui/button';

export function Header() {
  const handleSignOut = async () => {
    await signOut({
      callbackUrl: '/login',
      redirect: true,
    });
  };

  return (
    <header className="sticky top-0 z-50 w-full border-b border-gray-200 bg-white">
      <div className="flex h-16 items-center justify-between px-4">
        <div className="flex items-center gap-2">
          <h1 className="text-xl font-semibold">Infra Chatbot</h1>
        </div>
        <div className="flex items-center gap-4">
          <Button
            variant="ghost"
            onClick={handleSignOut}
            className="flex items-center gap-2"
          >
            <ArrowRightOnRectangleIcon className="h-5 w-5" />
            <span>Sign out</span>
          </Button>
        </div>
      </div>
    </header>
  );
}
