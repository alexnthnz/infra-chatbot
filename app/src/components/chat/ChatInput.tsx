import { useRef, KeyboardEvent, useState } from 'react';
import { cn } from '@/lib/utils';
import {
  PaperAirplaneIcon,
  MicrophoneIcon,
  PhotoIcon,
  LinkIcon,
  PaperClipIcon,
} from '@heroicons/react/24/outline';
import { Textarea } from '@/components/ui/textarea';
import { Button } from '@/components/ui/button';
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from '@/components/ui/tooltip';

interface ChatInputProps {
  isLoading: boolean;
  onSubmit: (message: string) => void;
  disabled?: boolean;
}

export function ChatInput({ isLoading, onSubmit, disabled }: ChatInputProps) {
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const [isTyping, setIsTyping] = useState(false);

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
      setIsTyping(false);
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

    setIsTyping(textarea.value.trim().length > 0);
  };

  return (
    <form onSubmit={handleSubmit} className="px-3 py-2">
      <div
        className={cn(
          'flex items-end gap-1.5 bg-white border border-gray-200 rounded-lg shadow-sm',
          'focus-within:ring-1 focus-within:ring-indigo-500 focus-within:border-indigo-500'
        )}
      >
        <div className="flex items-center space-x-1 px-2 py-1.5">
          <TooltipProvider>
            <Tooltip>
              <TooltipTrigger asChild>
                <Button
                  type="button"
                  variant="ghost"
                  size="sm"
                  className="h-7 w-7 p-0 text-gray-400 hover:text-gray-600"
                >
                  <PaperClipIcon className="h-4 w-4" />
                </Button>
              </TooltipTrigger>
              <TooltipContent side="top">
                <p className="text-xs">Attach file</p>
              </TooltipContent>
            </Tooltip>
          </TooltipProvider>

          <TooltipProvider>
            <Tooltip>
              <TooltipTrigger asChild>
                <Button
                  type="button"
                  variant="ghost"
                  size="sm"
                  className="h-7 w-7 p-0 text-gray-400 hover:text-gray-600"
                >
                  <PhotoIcon className="h-4 w-4" />
                </Button>
              </TooltipTrigger>
              <TooltipContent side="top">
                <p className="text-xs">Add image</p>
              </TooltipContent>
            </Tooltip>
          </TooltipProvider>

          <TooltipProvider>
            <Tooltip>
              <TooltipTrigger asChild>
                <Button
                  type="button"
                  variant="ghost"
                  size="sm"
                  className="h-7 w-7 p-0 text-gray-400 hover:text-gray-600"
                >
                  <LinkIcon className="h-4 w-4" />
                </Button>
              </TooltipTrigger>
              <TooltipContent side="top">
                <p className="text-xs">Add link</p>
              </TooltipContent>
            </Tooltip>
          </TooltipProvider>
        </div>

        <Textarea
          ref={textareaRef}
          rows={1}
          name="message"
          placeholder="Message infrastructure assistant..."
          disabled={isLoading || disabled}
          autoComplete="off"
          autoCorrect="off"
          autoCapitalize="off"
          spellCheck="false"
          onKeyDown={handleKeyDown}
          onChange={adjustHeight}
          className={cn(
            'flex-1 py-2 px-2 text-sm',
            'bg-transparent border-0',
            'text-gray-900 placeholder:text-gray-500',
            'focus-visible:outline-none focus-visible:ring-0 focus-visible:ring-offset-0',
            'disabled:opacity-50',
            'resize-none',
            'min-h-[38px] max-h-[100px]',
            'overflow-y-auto'
          )}
        />

        <div className="flex items-center pr-2 pl-1 py-1.5">
          {!isTyping ? (
            <TooltipProvider>
              <Tooltip>
                <TooltipTrigger asChild>
                  <Button
                    type="button"
                    variant="ghost"
                    size="sm"
                    className="h-7 w-7 p-0 text-gray-400 hover:text-gray-600"
                  >
                    <MicrophoneIcon className="h-4 w-4" />
                  </Button>
                </TooltipTrigger>
                <TooltipContent side="top">
                  <p className="text-xs">Voice input</p>
                </TooltipContent>
              </Tooltip>
            </TooltipProvider>
          ) : (
            <Button
              type="submit"
              variant="ghost"
              size="sm"
              disabled={isLoading || disabled}
              className="h-7 w-7 p-0 text-indigo-600 hover:text-indigo-700 hover:bg-indigo-50"
            >
              <PaperAirplaneIcon className={cn('h-4 w-4', isLoading && 'animate-pulse')} />
              <span className="sr-only">{isLoading ? 'Sending...' : 'Send message'}</span>
            </Button>
          )}
        </div>
      </div>

      <div className="flex justify-center mt-1">
        <p className="text-xs text-gray-500">Shift + Enter for new line</p>
      </div>
    </form>
  );
}
