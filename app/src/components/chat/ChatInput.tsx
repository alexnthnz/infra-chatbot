import { FormEvent, useRef, KeyboardEvent } from 'react';
import { cn } from '@/lib/utils';
import { LuSend } from 'react-icons/lu';

interface ChatInputProps {
  isLoading: boolean;
  onSubmit: (message: string) => void;
  disabled?: boolean;
}

export function ChatInput({ isLoading, onSubmit, disabled }: ChatInputProps) {
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const textarea = textareaRef.current;
    if (!textarea) return;

    const message = textarea.value.trim();
    if (message) {
      onSubmit(message);
      textarea.value = '';
      textarea.focus();
      // Reset height after clearing
      textarea.style.height = 'auto';
    }
  };

  const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      const form = e.currentTarget.form;
      form?.requestSubmit();
    }
  };

  const adjustHeight = () => {
    const textarea = textareaRef.current;
    if (!textarea) return;

    textarea.style.height = 'auto';
    textarea.style.height = `${textarea.scrollHeight}px`;
  };

  return (
    <form onSubmit={handleSubmit} className="p-2">
      <div className={cn('bg-gray-100', 'focus:outline-none focus:ring-2 focus:ring-gray-200')}>
        <textarea
          ref={textareaRef}
          rows={1}
          name="message"
          placeholder="Ask the agent something..."
          disabled={isLoading || disabled}
          autoComplete="off"
          autoCorrect="off"
          autoCapitalize="off"
          spellCheck="false"
          onKeyDown={handleKeyDown}
          onChange={adjustHeight}
          className={cn(
            'w-full p-3 pr-12 text-sm rounded-lg',
            'bg-gray-100 border-0',
            'text-gray-900 placeholder:text-gray-500',
            'focus:outline-none focus:ring-0 focus:border-0',
            'disabled:opacity-50',
            'resize-none',
            'max-h-96',
            'overflow-y-auto'
          )}
        />
        <div className="flex justify-end">
          <button
            type="submit"
            disabled={isLoading || disabled}
            className={cn(
              'p-2 rounded-lg',
              'text-gray-500 hover:text-gray-900 bg-transparent',
              'focus:outline-none',
              'disabled:opacity-50 disabled:hover:text-gray-500',
              'transition-colors'
            )}
          >
            <LuSend className={cn('h-5 w-5', isLoading && 'animate-pulse')} />
            <span className="sr-only">{isLoading ? 'Sending...' : 'Send message'}</span>
          </button>
        </div>
      </div>
    </form>
  );
}
