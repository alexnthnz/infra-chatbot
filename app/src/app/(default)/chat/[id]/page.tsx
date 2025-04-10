'use client';

import { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import { Card } from '@/components/ui/card';
import { ScrollArea } from '@/components/ui/scroll-area';
import { ChatHeader } from '@/components/chat/ChatHeader';
import { ChatInput } from '@/components/chat/ChatInput';
import { ChatMessage } from '@/components/chat/ChatMessage';

// Mock data for demonstration purposes
interface Message {
  id: string;
  content: string;
  role: 'user' | 'assistant';
}

export default function ChatPage() {
  const params = useParams();
  const chatId = params.id as string;
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [chatTitle, setChatTitle] = useState('Kubernetes Setup');

  useEffect(() => {
    // Mock fetching chat history
    const mockMessages: Message[] = [
      {
        id: '1',
        content: 'Hello, how can I help you with your infrastructure?',
        role: 'assistant',
      },
      { id: '2', content: 'I need help setting up a Kubernetes cluster', role: 'user' },
      {
        id: '3',
        content:
          'Sure, I can help with that. What specific aspects of Kubernetes cluster setup do you need assistance with?',
        role: 'assistant',
      },
    ];

    setMessages(mockMessages);
  }, [chatId]);

  const handleSendMessage = (content: string) => {
    if (!content.trim()) return;

    // Add user message
    const userMessage: Message = {
      id: Date.now().toString(),
      content,
      role: 'user',
    };

    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);

    // Simulate assistant response
    setTimeout(() => {
      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        content: `I'll help you with: "${content}"`,
        role: 'assistant',
      };

      setMessages(prev => [...prev, assistantMessage]);
      setIsLoading(false);
    }, 1000);
  };

  // Clear chat messages
  const handleClearChat = () => {
    setMessages([]);
  };

  // Create a new chat (in a real app, this would redirect to a new chat)
  const handleNewChat = () => {
    alert('Creating a new chat...');
    // In a real app: router.push('/chat/new');
  };

  return (
    <div className="flex flex-col h-full overflow-hidden">
      <div className="flex-shrink-0">
        <ChatHeader
          title={chatTitle}
          isLoading={isLoading}
          onClearChat={handleClearChat}
          onNewChat={handleNewChat}
        />
      </div>

      <div className="flex-grow overflow-hidden relative">
        <ScrollArea className="absolute inset-0 px-4 py-6">
          <div className="space-y-4">
            {messages.map(message => (
              <ChatMessage key={message.id} content={message.content} role={message.role} />
            ))}
            {isLoading && (
              <div className="flex justify-start px-4 py-2">
                <Card className="px-4 py-2 max-w-[85%] bg-gray-100">
                  <p className="text-sm">Typing...</p>
                </Card>
              </div>
            )}
          </div>
        </ScrollArea>
      </div>

      <div className="flex-shrink-0 border-t border-gray-200">
        <ChatInput isLoading={isLoading} onSubmit={handleSendMessage} />
      </div>
    </div>
  );
}
