'use client';

import { usePathname } from 'next/navigation';

export default function DefaultLayout({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();

  // Extract chat ID from the pathname if it's a chat route
  const chatIdMatch = pathname.match(/\/chat\/(.+)/);
  const currentChatId = chatIdMatch ? chatIdMatch[1] : undefined;

  return (
    <div className="flex flex-col overflow-hidden w-full h-screen">
      <header className="sticky top-0 z-50 w-full border-b border-gray-200 bg-white">
        <div className="flex h-16 items-center justify-between px-4">
          <div className="flex items-center gap-2">
            <h1 className="text-xl font-semibold">DeepFlow</h1>
          </div>
        </div>
      </header>
      <main className="flex-grow overflow-hidden h-full">
        {children}
      </main>
    </div>
  );
}
