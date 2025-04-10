import { ScrollArea } from '@/components/ui/scroll-area';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Separator } from '@/components/ui/separator';
import { ChatList } from '@/components/chat/ChatList';
import { ResourcesList } from '@/components/chat/ResourcesList';
import {
  Sidebar as UISidebar,
  SidebarContent as UISidebarContent,
  SidebarFooter,
  SidebarHeader,
} from '@/components/ui/sidebar';

interface ChatItem {
  id: string;
  title: string;
  lastMessage: string;
  updated: string;
}

interface Resource {
  id: string;
  title: string;
  description: string;
  url?: string;
  type: 'documentation' | 'template' | 'guide' | 'other';
}

interface SidebarProps {
  chats: ChatItem[];
  resources: Resource[];
  currentChatId?: string;
}

export function Sidebar({ chats, resources, currentChatId }: SidebarProps) {
  const SidebarContent = () => (
    <div className="h-full flex flex-col">
      <Tabs defaultValue="chats" className="w-full h-full flex flex-col">
        <div className="px-4 py-0.5 flex-shrink-0">
          <TabsList className="grid w-full grid-cols-2">
            <TabsTrigger value="chats">Chats</TabsTrigger>
            <TabsTrigger value="resources">Resources</TabsTrigger>
          </TabsList>
        </div>

        <Separator />

        <div className="flex-grow overflow-hidden">
          <ScrollArea className="h-full p-4">
            <TabsContent value="chats" className="mt-0">
              <ChatList chats={chats} currentChatId={currentChatId} />
            </TabsContent>

            <TabsContent value="resources" className="mt-0">
              <ResourcesList resources={resources} />
            </TabsContent>
          </ScrollArea>
        </div>
      </Tabs>
    </div>
  );

  return (
    <UISidebar>
      <SidebarHeader />
      <UISidebarContent>
        <SidebarContent />
      </UISidebarContent>
      <SidebarFooter />
    </UISidebar>
  );
}
