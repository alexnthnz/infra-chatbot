import { Card } from '@/components/ui/card';
import { ArrowTopRightOnSquareIcon } from '@heroicons/react/24/outline';

interface Resource {
  id: string;
  title: string;
  description: string;
  url?: string;
  type: 'documentation' | 'template' | 'guide' | 'other';
}

interface ResourcesListProps {
  resources: Resource[];
}

export function ResourcesList({ resources }: ResourcesListProps) {
  return (
    <div className="space-y-2">
      <div className="flex items-center justify-between mb-2">
        <h3 className="text-lg font-medium">Related Resources</h3>
      </div>

      {resources.length === 0 ? (
        <p className="text-sm text-gray-500 py-4 text-center">
          No resources available for this conversation.
        </p>
      ) : (
        <div className="space-y-3">
          {resources.map(resource => (
            <Card key={resource.id} className="p-3">
              <div className="flex justify-between">
                <h4 className="font-medium">{resource.title}</h4>
                {resource.url && (
                  <a
                    href={resource.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-indigo-600 hover:text-indigo-800"
                  >
                    <ArrowTopRightOnSquareIcon className="h-4 w-4" />
                  </a>
                )}
              </div>
              <p className="text-sm text-gray-500 mt-1">{resource.description}</p>
              <div className="mt-2">
                <span className="inline-flex items-center rounded-full bg-blue-50 px-2 py-1 text-xs font-medium text-blue-700">
                  {resource.type}
                </span>
              </div>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}
