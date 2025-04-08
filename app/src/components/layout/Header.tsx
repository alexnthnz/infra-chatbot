'use client';

import { IoLogOutOutline } from 'react-icons/io5';
import { signOut } from 'next-auth/react';

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
          <button
            onClick={handleSignOut}
            className="flex items-center gap-2 px-3 py-2 text-sm text-gray-700 hover:text-gray-900 rounded-md hover:bg-gray-100"
          >
            <IoLogOutOutline className="h-5 w-5" />
            <span>Sign out</span>
          </button>
        </div>
      </div>
    </header>
  );
}
