import { cn } from '@/lib/utils';

interface ChatMessageProps {
  content: string;
  role: 'user' | 'assistant';
}

export function ChatMessage({ content, role }: ChatMessageProps) {
  return (
    <div className={cn('flex w-full justify-start px-4 py-2', role === 'user' && 'justify-end')}>
      <div
        className={cn(
          'rounded-2xl px-4 py-2 max-w-[85%]',
          role === 'assistant' ? 'bg-gray-100 text-gray-900' : 'bg-black text-white'
        )}
      >
        <p className="text-sm whitespace-pre-wrap">{content}</p>
      </div>
    </div>
  );
}
