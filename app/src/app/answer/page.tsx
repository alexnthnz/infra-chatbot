'use client';

import { useState, useRef, useEffect } from 'react';

export default function Home() {
  const [question, setQuestion] = useState('');
  const [streamOutput, setStreamOutput] = useState<string[]>([]);
  const [isStreaming, setIsStreaming] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const eventSourceRef = useRef<EventSource | null>(null);

  // Function to unescape newlines
  const unescapeNewlines = (text: string): string => {
    return text
      .replace(/\\n/g, '\n') // Replace escaped \n with actual newline
      .replace(/\\r/g, '\r') // Handle carriage returns if present
      .replace(/\\\\/g, '\\'); // Handle double backslashes
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!question.trim()) {
      setError('Please enter a question');
      return;
    }

    setError(null);
    setStreamOutput([]);
    setIsStreaming(true);

    try {
      const apiUrl =
        'https://71fxbdvir6.execute-api.ap-southeast-2.amazonaws.com/api/v1/chats/messages';
      const formData = new FormData();
      formData.append('content', question);

      const response = await fetch(apiUrl, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const reader = response.body?.getReader();
      const decoder = new TextDecoder();
      let accumulatedChunk = '';

      while (reader) {
        const { done, value } = await reader.read();
        if (done) {
          setIsStreaming(false);
          break;
        }

        const chunk = decoder.decode(value, { stream: true });
        accumulatedChunk += chunk;

        const events = accumulatedChunk.split('\n\n');
        accumulatedChunk = events.pop() || '';

        for (const event of events) {
          if (event.startsWith('data:')) {
            const data = event.replace(/^data:\s*/, '').trim();
            if (data) {
              // Unescape newlines before adding to streamOutput
              const unescapedData = unescapeNewlines(data);
              setStreamOutput(prev => [...prev, unescapedData]);
            }
          }
        }
      }
    } catch (err) {
      setError(`Failed to fetch response: ${err.message}`);
      setIsStreaming(false);
    }
  };

  useEffect(() => {
    return () => {
      if (eventSourceRef.current) {
        eventSourceRef.current.close();
        eventSourceRef.current = null;
      }
    };
  }, []);

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col items-center justify-center p-4 w-full">
      <div className="bg-white shadow-md rounded-lg p-6 w-full max-w-2xl">
        <h1 className="text-2xl font-bold mb-4 text-center">Chat with LangChain Agent</h1>

        <form onSubmit={handleSubmit} className="mb-6">
          <div className="flex flex-col gap-4">
            <textarea
              value={question}
              onChange={e => setQuestion(e.target.value)}
              placeholder="Ask a question (e.g., What is the capital of France?)"
              className="w-full p-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 resize-y"
              rows={4}
              disabled={isStreaming}
            />
            <button
              type="submit"
              className={`w-full py-2 px-4 rounded-lg text-white font-semibold ${
                isStreaming ? 'bg-gray-400 cursor-not-allowed' : 'bg-blue-500 hover:bg-blue-600'
              }`}
              disabled={isStreaming}
            >
              {isStreaming ? 'Thinking...' : 'Send Question'}
            </button>
          </div>
        </form>

        {error && <div className="mb-4 p-3 bg-red-100 text-red-700 rounded-lg">{error}</div>}

        {streamOutput.length > 0 && (
          <div className="bg-gray-50 p-4 rounded-lg">
            <h2 className="text-lg font-semibold mb-2">Agent Response</h2>
            <div className="space-y-2 overflow-y-auto h-96">
              {streamOutput.map((chunk, index) => (
                <div key={index} className="p-3 bg-white border rounded-lg shadow-sm">
                  <div className="text-gray-800 whitespace-pre-wrap text-justify">{chunk}</div>
                </div>
              ))}
            </div>
            {isStreaming && (
              <div className="mt-2 text-gray-500 animate-pulse">Waiting for more chunks...</div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
