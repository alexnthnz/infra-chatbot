'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { useSetAtom } from 'jotai';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import {
  MicrophoneIcon,
  ChevronDownIcon,
  SquaresPlusIcon,
  PhotoIcon,
  ArrowUpTrayIcon,
  DocumentTextIcon,
  UserGroupIcon,
} from '@heroicons/react/24/outline';
import { sendMessage } from '@/actions/chat';
import { initChatSessionAtom } from '@/store/chat';

export default function HomePage() {
  const router = useRouter();
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  
  // Get the setter function for initializing a chat session
  const initChatSession = useSetAtom(initChatSessionAtom);

  const handleButtonClick = (action: string) => {
    // In a real app, you would implement the actual functionality here
  };

  const handleSendMessage = async () => {
    if (!inputValue.trim() || isLoading) return;
    
    setIsLoading(true);
    
    try {
      // First message is always a new chat
      const result = await sendMessage({
        content: inputValue,
        is_new_chat: true,
        response_type: 'json'
      });
      
      if (!result.success || !result.data) {
        throw new Error(result.error || 'Failed to send message');
      }
      
      // Get data directly from the response
      const { message, session_id } = result.data;
      
      if (!session_id) {
        throw new Error('No session ID received from the server');
      }
      
      // Initialize the chat session in Jotai store with both user and assistant messages
      initChatSession({ 
        sessionId: session_id, 
        initialUserMessage: inputValue,
        initialMessage: message 
      });
      
      // Redirect to the chat page with the session ID
      router.push(`/chat/${session_id}`);
    } catch (error) {
      console.error('Error sending message:', error);
      alert(`Error: ${error instanceof Error ? error.message : 'Unknown error'}`);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen p-8 max-w-4xl mx-auto">
      <div className="w-full flex justify-end mb-4">
        <Button 
          variant="outline" 
          onClick={() => router.push('/chats')}
          className="rounded-full text-base"
        >
          View Chat History
        </Button>
      </div>
    
      <h1 className="text-5xl font-bold mb-10 text-center">What can I help you ship?</h1>

      <div className="w-full mb-10 bg-white rounded-lg border border-gray-200 p-6 shadow-sm">
        <div className="flex items-center">
          <Input
            type="text"
            placeholder="Ask me to build..."
            className="border-none shadow-none focus-visible:ring-0 text-lg py-6"
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

          <div className="flex items-center ml-auto">
            <Select>
              <SelectTrigger className="w-[180px] border-none text-base">
                <SelectValue placeholder="No project selected" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="no-project">No project selected</SelectItem>
                <SelectItem value="new-project">Create new project</SelectItem>
              </SelectContent>
            </Select>

            <div className="flex ml-2 space-x-1">
              <Button 
                variant="ghost" 
                size="icon" 
                className="h-10 w-10"
                onClick={handleSendMessage}
                disabled={isLoading || !inputValue.trim()}
              >
                {isLoading ? (
                  <div className="h-6 w-6 border-t-2 border-b-2 border-indigo-500 rounded-full animate-spin" />
                ) : (
                  <MicrophoneIcon className="h-6 w-6" />
                )}
              </Button>
              <Button variant="ghost" size="icon" className="h-10 w-10">
                <ChevronDownIcon className="h-6 w-6" />
              </Button>
            </div>
          </div>
        </div>
      </div>

      <div className="flex flex-wrap justify-center gap-4">
        <Button 
          variant="outline" 
          className="rounded-full text-base py-6 px-6"
          onClick={() => handleButtonClick('clone-screenshot')}
        >
          <PhotoIcon className="h-5 w-5 mr-2" />
          Clone a Screenshot
        </Button>
        <Button 
          variant="outline" 
          className="rounded-full text-base py-6 px-6"
          onClick={() => handleButtonClick('import-figma')}
        >
          <SquaresPlusIcon className="h-5 w-5 mr-2" />
          Import from Figma
        </Button>
        <Button 
          variant="outline" 
          className="rounded-full text-base py-6 px-6"
          onClick={() => handleButtonClick('upload-project')}
        >
          <ArrowUpTrayIcon className="h-5 w-5 mr-2" />
          Upload a Project
        </Button>
        <Button 
          variant="outline" 
          className="rounded-full text-base py-6 px-6"
          onClick={() => handleButtonClick('landing-page')}
        >
          <DocumentTextIcon className="h-5 w-5 mr-2" />
          Landing Page
        </Button>
        <Button 
          variant="outline" 
          className="rounded-full text-base py-6 px-6"
          onClick={() => handleButtonClick('signup-form')}
        >
          <UserGroupIcon className="h-5 w-5 mr-2" />
          Sign Up Form
        </Button>
      </div>
    </div>
  );
}
