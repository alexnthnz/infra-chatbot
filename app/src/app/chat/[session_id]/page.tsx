'use client';

import { useEffect, useState, useMemo, useRef } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { useAtom, useSetAtom } from 'jotai';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { sendMessage } from '@/actions/chat';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card } from '@/components/ui/card';
import { 
  getChatSessionAtom, 
  addMessageAtom, 
  setLoadingAtom, 
  initChatSessionAtom,
  Message
} from '@/store/chat';

// Chat message component
function ChatMessage({ role, content }: { role: 'user' | 'assistant'; content: string }) {
  return (
    <div className={`flex ${role === 'user' ? 'justify-end' : 'justify-start'} mb-6`}>
      <Card
        className={`p-5 max-w-[85%] ${
          role === 'user' ? 'bg-indigo-600 text-white' : 'bg-white border border-gray-200 shadow-sm'
        }`}
      >
        {role === 'assistant' ? (
          <div className="prose">
            <ReactMarkdown
              remarkPlugins={[remarkGfm]}
              components={{
                // Override default component renderers
                a: ({ node, ...props }: { node?: any; className?: string } & React.HTMLAttributes<HTMLAnchorElement>) => (
                  <a 
                    {...props} 
                    target="_blank" 
                    rel="noopener noreferrer"
                    className="text-blue-600 hover:underline"
                  />
                ),
                code: ({ node, inline, ...props }: { node?: any; inline?: boolean; className?: string } & React.HTMLAttributes<HTMLElement>) => (
                  inline 
                    ? <code {...props} className="bg-gray-200 px-1 py-0.5 rounded text-sm font-mono" />
                    : <code {...props} className="block bg-gray-800 text-gray-200 p-3 rounded-md overflow-x-auto my-3 text-sm font-mono" />
                ),
                p: ({ node, ...props }: { node?: any } & React.HTMLAttributes<HTMLParagraphElement>) => (
                  <p {...props} className="text-base leading-relaxed my-3" />
                ),
                ul: ({ node, ...props }: { node?: any } & React.HTMLAttributes<HTMLUListElement>) => (
                  <ul {...props} className="list-disc pl-6 my-3 text-base" />
                ),
                ol: ({ node, ...props }: { node?: any } & React.HTMLAttributes<HTMLOListElement>) => (
                  <ol {...props} className="list-decimal pl-6 my-3 text-base" />
                ),
                li: ({ node, ...props }: { node?: any } & React.HTMLAttributes<HTMLLIElement>) => (
                  <li {...props} className="my-1.5 text-base" />
                ),
                h1: ({ node, ...props }: { node?: any } & React.HTMLAttributes<HTMLHeadingElement>) => (
                  <h1 {...props} className="text-2xl font-bold my-4" />
                ),
                h2: ({ node, ...props }: { node?: any } & React.HTMLAttributes<HTMLHeadingElement>) => (
                  <h2 {...props} className="text-xl font-bold my-3" />
                ),
                h3: ({ node, ...props }: { node?: any } & React.HTMLAttributes<HTMLHeadingElement>) => (
                  <h3 {...props} className="text-lg font-bold my-3" />
                ),
              }}
            >
              {content}
            </ReactMarkdown>
          </div>
        ) : (
          <p className="text-base leading-relaxed">{content}</p>
        )}
      </Card>
    </div>
  );
}

export default function ChatPage() {
  const params = useParams();
  const router = useRouter();
  const session_id = params.session_id as string;
  
  const [inputValue, setInputValue] = useState('');
  const [sessionInitialized, setSessionInitialized] = useState(false);
  
  // Create a ref for the message container
  const messagesEndRef = useRef<HTMLDivElement>(null);
  
  // Memoize the session atom to prevent recreation on each render
  const sessionAtom = useMemo(() => getChatSessionAtom(session_id), [session_id]);
  
  // Initialize Jotai atoms
  const [session] = useAtom(sessionAtom);
  const addMessage = useSetAtom(addMessageAtom);
  const setLoading = useSetAtom(setLoadingAtom);
  const initSession = useSetAtom(initChatSessionAtom);

  // Extract values from session atom
  const { messages, isLoading } = session;
  
  // Scroll to bottom whenever messages change
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };
  
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // On page load, add the initial message from the server if this is a new conversation
  useEffect(() => {
    // Skip initialization if we already have messages
    if (sessionInitialized || messages.length > 0) return;
    
    // Just initialize the session without relying on URL parameters
    initSession({ sessionId: session_id });
    
    setSessionInitialized(true);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [session_id, messages.length]);

  // Handle sending a message in the chat
  const handleSendMessage = async () => {
    if (!inputValue.trim() || isLoading) return;
    
    setLoading({ sessionId: session_id, isLoading: true });
    
    // Add user message immediately to the UI
    const userMessage: Message = {
      role: 'user',
      content: inputValue,
      timestamp: new Date().toISOString()
    };
    
    addMessage({ sessionId: session_id, message: userMessage });
    const messageContent = inputValue;
    setInputValue(''); // Clear input right away
    
    try {
      // Call the server action
      const result = await sendMessage({
        content: messageContent,
        is_new_chat: false,
        session_id: session_id,
        response_type: 'json'
      });
      
      if (!result.success || !result.data) {
        throw new Error(result.error || 'Failed to send message');
      }
      
      // Get data directly from the response
      const { message } = result.data;
      
      // Add assistant's response to the messages
      const assistantMessage: Message = {
        role: 'assistant',
        content: message,
        timestamp: new Date().toISOString()
      };
      
      addMessage({ sessionId: session_id, message: assistantMessage });
    } catch (error) {
      console.error('Error sending message:', error);
      // Add error message
      addMessage({
        sessionId: session_id,
        message: {
          role: 'assistant',
          content: `Error: ${error instanceof Error ? error.message : 'Unknown error'}`,
          timestamp: new Date().toISOString()
        }
      });
    } finally {
      setLoading({ sessionId: session_id, isLoading: false });
    }
  };

  // Go back to home page to start a new chat
  const handleNewChat = () => {
    router.push('/');
  };

  return (
    <div className="flex flex-col h-screen">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 p-4 shadow-sm">
        <div className="max-w-5xl mx-auto flex justify-between items-center">
          <h1 className="text-xl font-semibold">Chat Session: {session_id.substring(0, 8)}...</h1>
          <div className="flex space-x-2">
            <Button variant="outline" onClick={() => router.push('/chats')}>
              All Chats
            </Button>
            <Button variant="outline" onClick={handleNewChat}>
              New Chat
            </Button>
          </div>
        </div>
      </header>
      
      {/* Chat messages container */}
      <main className="flex-1 p-6 overflow-auto bg-gray-50">
        <div className="max-w-5xl mx-auto space-y-6">
          {messages
            .slice() // Create a copy to avoid mutating the original
            .map((message, index) => (
              <ChatMessage
                key={index}
                role={message.role}
                content={message.content}
              />
            ))}
          
          {isLoading && (
            <div className="flex justify-start mb-4">
              <Card className="px-4 py-3 bg-gray-100 max-w-[80%]">
                <div className="flex items-center space-x-2">
                  <div className="h-2 w-2 bg-gray-500 rounded-full animate-bounce" />
                  <div className="h-2 w-2 bg-gray-500 rounded-full animate-bounce delay-150" />
                  <div className="h-2 w-2 bg-gray-500 rounded-full animate-bounce delay-300" />
                </div>
              </Card>
            </div>
          )}
          
          {/* Invisible element to scroll to */}
          <div ref={messagesEndRef} />
        </div>
      </main>
      
      {/* Input area */}
      <footer className="bg-white border-t border-gray-200 p-6 shadow-inner">
        <div className="max-w-5xl mx-auto flex gap-3">
          <Input
            className="flex-1 text-base py-6"
            placeholder="Type a message..."
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                handleSendMessage();
              }
            }}
            disabled={isLoading}
          />
          <Button 
            onClick={handleSendMessage}
            disabled={!inputValue.trim() || isLoading}
            className="px-6"
          >
            Send
          </Button>
        </div>
      </footer>
    </div>
  );
} 