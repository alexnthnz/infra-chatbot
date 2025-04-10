'use client';

import { usePathname } from 'next/navigation';
import { Header } from '@/components/layout/Header';
import { Sidebar } from '@/components/layout/Sidebar';

// Mock data for the sidebar
const mockChats = [
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

const mockResources = [
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

export default function DefaultLayout({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();

  // Extract chat ID from the pathname if it's a chat route
  const chatIdMatch = pathname.match(/\/chat\/(.+)/);
  const currentChatId = chatIdMatch ? chatIdMatch[1] : undefined;

  return (
    <>
      <Sidebar chats={mockChats} resources={mockResources} currentChatId={currentChatId} />
      <div className="flex flex-col overflow-hidden w-full h-screen">
        <Header />
        <main className="flex-grow overflow-hidden h-full">
          {children}
        </main>
      </div>
    </>
  );
}
