import Link from 'next/link';
import { cn } from '@/lib/utils';
import { ChatBubbleLeftRightIcon, PlusIcon } from '@heroicons/react/24/outline';
import { Button } from '@/components/ui/button';

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
    <div className="w-full">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-medium">Recent Chats</h3>
        <Link href="/chat">
          <Button size="sm" variant="outline" className="h-8 gap-1">
            <PlusIcon className="h-4 w-4" />
          </Button>
        </Link>
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
        <ul className="space-y-1 w-full">
          {chats.map(chat => (
            <li key={chat.id} className="w-full">
              <Link 
                href={`/chat/${chat.id}`} 
                className={cn(
                  "flex flex-col w-full p-2 rounded-md hover:bg-gray-100 transition-colors",
                  currentChatId === chat.id && "bg-gray-200"
                )}
              >
                <div className="flex justify-between items-center w-full">
                  <span className="font-medium text-sm truncate mr-2">{chat.title}</span>
                </div>
                <p className="text-xs text-gray-500 line-clamp-1 w-full mt-1">{chat.lastMessage}</p>
              </Link>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
