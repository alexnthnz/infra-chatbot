import { cn } from '@/lib/utils';
import { Card } from '@/components/ui/card';

interface ChatMessageProps {
  content: string;
  role: 'user' | 'assistant';
}

export function ChatMessage({ content, role }: ChatMessageProps) {
  return (
    <div className={cn('flex w-full justify-start px-4 py-2', role === 'user' && 'justify-end')}>
      <Card
        className={cn(
          'px-4 py-2 max-w-[85%]',
          role === 'assistant' ? 'bg-gray-100' : 'bg-black text-white'
        )}
      >
        <p className="text-sm whitespace-pre-wrap">{content}</p>
      </Card>
    </div>
  );
}
