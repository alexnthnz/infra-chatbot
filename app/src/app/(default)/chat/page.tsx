'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { Card } from '@/components/ui/card';
import { Skeleton } from '@/components/ui/skeleton';

export default function ChatIndexPage() {
  const router = useRouter();

  useEffect(() => {
    // In a real app, you would create a new chat via API and get its ID
    const newChatId = '1'; // Using a mock ID for now
    router.push(`/chat/${newChatId}`);
  }, [router]);

  // Show a loading state while redirecting
  return (
    <div className="h-screen flex items-center justify-center">
      <Card className="w-full max-w-md p-6">
        <div className="space-y-4">
          <Skeleton className="h-8 w-3/4 mx-auto" />
          <Skeleton className="h-4 w-full" />
          <Skeleton className="h-4 w-full" />
          <Skeleton className="h-4 w-2/3" />
        </div>
        <div className="mt-6 text-center text-sm text-gray-500">
          Creating a new chat session...
        </div>
      </Card>
    </div>
  );
} 