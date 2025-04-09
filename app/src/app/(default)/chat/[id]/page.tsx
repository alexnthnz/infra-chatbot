'use client';

import { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import * as ResizablePrimitive from 'react-resizable-panels';
import { Card } from '@/components/ui/card';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { ChatHeader } from '@/components/chat/ChatHeader';
import { ChatInput } from '@/components/chat/ChatInput';
import { ChatMessage } from '@/components/chat/ChatMessage';
import { ChatList } from '@/components/chat/ChatList';
import { ResourcesList } from '@/components/chat/ResourcesList';

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

  // Mock chat history
  const recentChats = [
    {
      id: '1',
      title: 'Kubernetes Setup',
      lastMessage: 'I need help setting up a Kubernetes cluster',
      updated: '1 hour ago',
    },
    {
      id: '2',
      title: 'Terraform Configuration',
      lastMessage: 'How do I configure AWS resources?',
      updated: '1 day ago',
    },
    {
      id: '3',
      title: 'CI/CD Pipeline',
      lastMessage: 'Can you help with GitHub Actions?',
      updated: '2 days ago',
    },
  ];

  // Mock resources
  const resources = [
    {
      id: '1',
      title: 'Kubernetes Documentation',
      description: 'Official docs for Kubernetes setup and configuration',
      url: 'https://kubernetes.io/docs/',
      type: 'documentation' as const,
    },
    {
      id: '2',
      title: 'Terraform Templates',
      description: 'Infrastructure templates for cloud providers',
      url: 'https://registry.terraform.io/',
      type: 'template' as const,
    },
    {
      id: '3',
      title: 'Deployment Guide',
      description: 'Step-by-step guide for Kubernetes deployments',
      type: 'guide' as const,
    },
  ];

  useEffect(() => {
    // Mock fetching chat history
    const mockMessages: Message[] = [
      { id: '1', content: 'Hello, how can I help you with your infrastructure?', role: 'assistant' },
      { id: '2', content: 'I need help setting up a Kubernetes cluster', role: 'user' },
      { id: '3', content: 'Sure, I can help with that. What specific aspects of Kubernetes cluster setup do you need assistance with?', role: 'assistant' },
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
    
    setMessages((prev) => [...prev, userMessage]);
    setIsLoading(true);
    
    // Simulate assistant response
    setTimeout(() => {
      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        content: `I'll help you with: "${content}"`,
        role: 'assistant',
      };
      
      setMessages((prev) => [...prev, assistantMessage]);
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
    <div className="h-screen flex flex-col overflow-hidden">
      <ResizablePrimitive.PanelGroup
        direction="horizontal"
        className="flex-grow"
      >
        {/* Left Panel - Sidebar */}
        <ResizablePrimitive.Panel defaultSize={25} minSize={20} maxSize={40}>
          <Card className="h-full border-0 rounded-none">
            <Tabs defaultValue="chats" className="w-full h-full flex flex-col">
              <div className="border-b px-4 py-2 flex-shrink-0">
                <TabsList className="grid w-full grid-cols-2">
                  <TabsTrigger value="chats">Chats</TabsTrigger>
                  <TabsTrigger value="resources">Resources</TabsTrigger>
                </TabsList>
              </div>
              
              <div className="flex-grow overflow-hidden">
                <ScrollArea className="h-full p-4">
                  <TabsContent value="chats" className="mt-0">
                    <ChatList chats={recentChats} currentChatId={chatId} />
                  </TabsContent>
                  
                  <TabsContent value="resources" className="mt-0">
                    <ResourcesList resources={resources} />
                  </TabsContent>
                </ScrollArea>
              </div>
            </Tabs>
          </Card>
        </ResizablePrimitive.Panel>
        
        <ResizablePrimitive.PanelResizeHandle className="w-2 bg-gray-200 hover:bg-gray-300" />
        
        {/* Right Panel - Chat Area */}
        <ResizablePrimitive.Panel defaultSize={75}>
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
                  {messages.map((message) => (
                    <ChatMessage
                      key={message.id}
                      content={message.content}
                      role={message.role}
                    />
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
              <ChatInput 
                isLoading={isLoading}
                onSubmit={handleSendMessage}
              />
            </div>
          </div>
        </ResizablePrimitive.Panel>
      </ResizablePrimitive.PanelGroup>
    </div>
  );
}
