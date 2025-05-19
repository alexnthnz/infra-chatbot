'use server';

import { z } from 'zod';
import { API_URL, ENDPOINTS } from '@/lib/api';

// Input validation schema with updated fields
const MessageSchema = z.object({
  content: z.string().min(1, 'Message cannot be empty'),
  is_new_chat: z.boolean().default(false),
  session_id: z.string().optional(),
  attachments: z.array(z.instanceof(File)).optional(),
}).refine(data => {
  // If not a new chat, session_id must be provided
  if (!data.is_new_chat && (!data.session_id || data.session_id.trim() === '')) {
    return false;
  }
  return true;
}, {
  message: 'Session ID is required when not creating a new chat',
  path: ['session_id'],
});

type Message = z.infer<typeof MessageSchema>;

/**
 * Send a new message to the chat API
 * This function returns the response data directly rather than a Response object
 * @param message The message content and other required fields
 * @returns The API response data or an error object
 */
export async function sendMessage(message: Message): Promise<{ 
  success: boolean; 
  data?: { 
    message: string; 
    session_id: string;
    resources: string[];
    images: string[];
  }; 
  error?: string 
}> {
  try {
    // Validate the input
    const validatedData = MessageSchema.parse(message);
    
    // Prepare the FormData for the API
    const formData = new FormData();
    formData.append('content', validatedData.content);
    formData.append('is_new_chat', validatedData.is_new_chat ? '1' : '0');
    
    // Only append session_id if it's not a new chat
    if (!validatedData.is_new_chat && validatedData.session_id) {
      formData.append('session_id', validatedData.session_id);
    }
    
    // Add attachments if provided - using the correct parameter name 'attachments'
    if (validatedData.attachments && validatedData.attachments.length > 0) {
      validatedData.attachments.forEach((file) => {
        formData.append('attachments', file);
      });
    }

    // Make the API request
    const response = await fetch(`${API_URL}${ENDPOINTS.MESSAGES}`, {
      method: 'POST',
      body: formData,
    });

    // Check if the request was successful
    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`Failed to send message: ${response.status} - ${errorText}`);
    }

    // Parse the JSON response
    const data = await response.json();
    
    // Return the data directly
    return { success: true, data };
  } catch (error) {
    // If it's a Zod validation error, return a friendly message
    if (error instanceof z.ZodError) {
      const errorMessage = error.errors.map(err => err.message).join(', ');
      return { success: false, error: errorMessage };
    }
    
    // For other errors, return the error message
    return { 
      success: false, 
      error: error instanceof Error ? error.message : 'An unknown error occurred' 
    };
  }
} 