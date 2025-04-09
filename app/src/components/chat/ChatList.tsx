import Link from 'next/link';
import { Card } from '@/components/ui/card';
import { cn } from '@/lib/utils';
import { ChatBubbleLeftRightIcon } from '@heroicons/react/24/outline';

interface ChatItem {
  id: string;
  title: string;
  lastMessage: string;
  updated: string;
}

interface ChatListProps {
  chats: ChatItem[];
  currentChatId?: string;
}

export function ChatList({ chats, currentChatId }: ChatListProps) {
  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-medium">Recent Chats</h3>
      </div>
      
      {chats.length === 0 ? (
        <div className="flex flex-col items-center justify-center py-8 text-center">
          <ChatBubbleLeftRightIcon className="h-12 w-12 text-gray-300 mb-2" />
          <h3 className="text-lg font-medium text-gray-900">No chats yet</h3>
          <p className="text-sm text-gray-500 mt-1">
            Start a new conversation to get help with infrastructure
          </p>
        </div>
      ) : (
        <div className="flex flex-col gap-4">
          {chats.map((chat) => (
            <Link key={chat.id} href={`/chat/${chat.id}`} className="block">
              <Card 
                className={cn(
                  "p-2.5 hover:bg-gray-50 transition-colors cursor-pointer",
                  currentChatId === chat.id ? "bg-gray-50 border-indigo-500 border-l-4" : "border-l-4 border-transparent"
                )}
              >
                <h4 className="font-medium text-sm truncate">{chat.title}</h4>
              </Card>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
} 