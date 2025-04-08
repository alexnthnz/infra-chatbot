export function ChatHeader() {
  return (
    <div className="flex items-center justify-between p-4 border-b border-gray-200">
      <div className="flex items-center gap-2">
        <h2 className="text-lg font-medium">Chat with Agent</h2>
      </div>
      <div className="flex items-center gap-2">
        {/* Add chat-specific controls here later if needed */}
      </div>
    </div>
  );
}
