'use client';

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

export default function Home() {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen p-5 max-w-3xl mx-auto">
      <h1 className="text-4xl font-bold mb-8">What can I help you ship?</h1>

      <div className="w-full mb-8 bg-white rounded-lg border border-gray-200 p-4">
        <div className="flex items-center">
          <Input
            type="text"
            placeholder="Ask v0 to build..."
            className="border-none shadow-none focus-visible:ring-0 text-base"
          />

          <div className="flex items-center ml-auto">
            <Select>
              <SelectTrigger className="w-[180px] border-none">
                <SelectValue placeholder="No project selected" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="no-project">No project selected</SelectItem>
              </SelectContent>
            </Select>

            <div className="flex ml-2 space-x-1">
              <Button variant="ghost" size="icon" className="h-8 w-8">
                <MicrophoneIcon className="h-5 w-5" />
              </Button>
              <Button variant="ghost" size="icon" className="h-8 w-8">
                <ChevronDownIcon className="h-5 w-5" />
              </Button>
            </div>
          </div>
        </div>
      </div>

      <div className="flex flex-wrap justify-center gap-3">
        <Button variant="outline" className="rounded-full">
          <PhotoIcon className="h-4 w-4 mr-2" />
          Clone a Screenshot
        </Button>
        <Button variant="outline" className="rounded-full">
          <SquaresPlusIcon className="h-4 w-4 mr-2" />
          Import from Figma
        </Button>
        <Button variant="outline" className="rounded-full">
          <ArrowUpTrayIcon className="h-4 w-4 mr-2" />
          Upload a Project
        </Button>
        <Button variant="outline" className="rounded-full">
          <DocumentTextIcon className="h-4 w-4 mr-2" />
          Landing Page
        </Button>
        <Button variant="outline" className="rounded-full">
          <UserGroupIcon className="h-4 w-4 mr-2" />
          Sign Up Form
        </Button>
      </div>
    </div>
  );
}
