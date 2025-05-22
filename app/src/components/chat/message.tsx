import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

import {AudioLines } from 'lucide-react';
import { Message } from '@/store/chat';
import { Card } from '../ui/card';

// Extended Message type to include attachments
interface ExtendedMessage extends Message {
    attachments?: {
        type: 'image' | 'audio' | 'other';
        url: string;
        name: string;
    }[];
}

export default function ChatMessage({ role, content, attachments, resources, images }: { 
    role: 'user' | 'assistant'; 
    content: string;
    attachments?: ExtendedMessage['attachments'];
    resources?: string[];
    images?: string[];
  }) {
    // Helper function to group resources by domain and count them
    const groupResourcesByDomain = (resources: string[]) => {
      const domainMap = new Map<string, number>();
      
      resources.forEach(url => {
        try {
          // Extract domain from URL
          const domain = new URL(url).hostname.replace(/^www\./, '');
          domainMap.set(domain, (domainMap.get(domain) || 0) + 1);
        } catch {
          // If URL parsing fails, use the original string
          domainMap.set(url, (domainMap.get(url) || 0) + 1);
        }
      });
      
      return Array.from(domainMap.entries()).map(([domain, count]) => ({
        domain,
        count
      }));
    };
  
    return (
      <div className={`flex flex-col ${role === 'user' ? 'items-end' : 'items-start'} mb-6`}>
        {role === 'user' ? (
          <Card
            className={`py-2 px-4 max-w-[85%] bg-indigo-600/70 text-white rounded-xl`}
          >
            <p className="text-base leading-relaxed">{content}</p>
          </Card>
        ) : (
          <div className="p-5 max-w-[85%]">
            {/* Display AI-generated images if available */}
            {images && images.length > 0 && (
              <div className="mb-4 grid grid-cols-2 md:grid-cols-3 gap-4">
                {images.map((imageUrl, index) => (
                  <div key={index} className="relative aspect-square rounded-lg overflow-hidden border border-gray-200">
                    <img
                      src={imageUrl}
                      alt={`Generated image ${index + 1}`}
                      className="w-full h-full object-cover"
                    />
                  </div>
                ))}
              </div>
            )}
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
            {resources && resources.length > 0 && (
              <div className="mt-4 flex flex-wrap gap-2">
                {groupResourcesByDomain(resources).map(({ domain }, index) => (
                  <span
                    key={index}
                    className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-blue-50 text-blue-700 border border-blue-100"
                  >
                    {domain}
                  </span>
                ))}
              </div>
            )}
          </div>
        )}
        
        {/* Display attachments if present - now outside the card */}
        {attachments && attachments.length > 0 && (
          <div className={`max-w-[85%] mt-2 ${role === 'user' ? 'mr-0' : 'ml-0'}`}>
            <div className="flex flex-wrap gap-2">
              {attachments.map((attachment, index) => (
                attachment.type === 'image' ? (
                  <div key={index} className="relative">
                    <div className="relative h-12 w-12 overflow-hidden rounded-md border border-gray-200 shadow-sm">
                      <img 
                        src={attachment.url} 
                        alt={attachment.name || `Attachment ${index + 1}`}
                        className="w-full h-full object-cover"
                      />
                    </div>
                  </div>
                ) : (
                  <div 
                    key={index}
                    className={`flex items-center gap-1 text-xs rounded-full px-3 py-1 ${
                      role === 'user' ? 'bg-indigo-500 text-white' : 'bg-gray-200 text-gray-700'
                    }`}
                  >
                    <AudioLines size={14} className={role === 'user' ? 'text-white' : 'text-gray-600'} /> 
                    <span>Audio Recording {index + 1}</span>
                  </div>
                )
              ))}
            </div>
          </div>
        )}
      </div>
    );
  }