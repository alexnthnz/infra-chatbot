'use client';

import { usePathname, useRouter } from 'next/navigation';
import { Button } from '@/components/ui/button';
import { PlusCircle, History } from 'lucide-react';

export default function DefaultLayout({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const router = useRouter();

  // Check if we're on the chats route or a specific chat session
  const isChatsRoute = pathname === '/chats';
  const isChatSessionRoute = pathname.startsWith('/chats/');

  return (
    <div className="flex flex-col overflow-hidden w-full h-screen">
      <header className="sticky top-0 z-50 w-full border-b border-gray-200 bg-white">
        <div className="flex h-16 items-center justify-between px-4">
          <div className="flex items-center gap-2">
            <h1 className="text-xl font-semibold">DeepFlow</h1>
          </div>
          <div className="flex items-center gap-2">
            {isChatSessionRoute && (
              <Button
                variant="outline"
                size="sm"
                onClick={() => router.push('/chats')}
                className="flex items-center gap-2"
              >
                <History className="h-4 w-4" />
                History
              </Button>
            )}
            {(isChatsRoute || isChatSessionRoute) && (
              <Button
                variant="default"
                size="sm"
                onClick={() => router.push('/')}
                className="flex items-center gap-2"
              >
                <PlusCircle className="h-4 w-4" />
                New Chat
              </Button>
            )}
          </div>
        </div>
      </header>
      <main className="flex-grow overflow-hidden h-full">
        {children}
      </main>
    </div>
  );
}
