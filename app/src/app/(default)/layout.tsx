'use client';

import { Header } from '@/components/layout/Header';
import { Panel, PanelGroup, PanelResizeHandle } from 'react-resizable-panels';

export default function DefaultLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex flex-col h-screen">
      <Header />
      <PanelGroup direction="horizontal" className="flex-1">
        {/* Left section - Chat */}
        <Panel defaultSize={50} minSize={30} className="flex flex-col">
          {children}
        </Panel>

        <PanelResizeHandle className="w-2 bg-gray-100 hover:bg-gray-200 transition-colors">
          <div className="w-0.5 h-full mx-auto bg-gray-200" />
        </PanelResizeHandle>

        {/* Right section - Empty for now */}
        <Panel defaultSize={50} minSize={30}>
          {/* Content for right section will be added later */}
        </Panel>
      </PanelGroup>
    </div>
  );
}
