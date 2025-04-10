import { Button } from '@/components/ui/button';
import {
  EllipsisHorizontalIcon,
  PlusCircleIcon,
  ShareIcon,
  ArrowPathIcon,
} from '@heroicons/react/24/outline';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';

interface ChatHeaderProps {
  title?: string;
  isLoading?: boolean;
  onClearChat?: () => void;
  onNewChat?: () => void;
}

export function ChatHeader({
  title = 'Infrastructure Assistant',
  isLoading = false,
  onClearChat,
  onNewChat,
}: ChatHeaderProps) {
  return (
    <div className="flex items-center justify-between px-4 py-2 border-b border-gray-200 bg-white">
      <div className="flex items-center">
        <div
          className={`w-2 h-2 rounded-full mr-2 ${isLoading ? 'bg-green-500 animate-pulse' : 'bg-indigo-600'}`}
        />
        <h2 className="text-base font-medium text-gray-900">{title}</h2>
      </div>

      <div className="flex items-center space-x-1">
        <Button
          variant="ghost"
          size="sm"
          className="h-7 w-7 p-0 text-gray-500 hover:text-gray-700"
          onClick={onNewChat}
        >
          <PlusCircleIcon className="h-4 w-4" />
          <span className="sr-only">New Chat</span>
        </Button>

        <Button variant="ghost" size="sm" className="h-7 w-7 p-0 text-gray-500 hover:text-gray-700">
          <ShareIcon className="h-4 w-4" />
          <span className="sr-only">Share</span>
        </Button>

        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <Button
              variant="ghost"
              size="sm"
              className="h-7 w-7 p-0 text-gray-500 hover:text-gray-700"
            >
              <EllipsisHorizontalIcon className="h-4 w-4" />
              <span className="sr-only">More options</span>
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent align="end">
            <DropdownMenuItem onClick={onClearChat} className="cursor-pointer text-xs">
              <ArrowPathIcon className="h-3.5 w-3.5 mr-2" />
              Clear chat
            </DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
      </div>
    </div>
  );
}
