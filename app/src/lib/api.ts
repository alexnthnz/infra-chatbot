/**
 * API configuration and utility functions
 */

// API URL configuration - can be overridden with environment variables
export const API_URL = process.env.API_URL || 'https://u2m4hpxzi9.execute-api.ap-southeast-2.amazonaws.com';
export const API_VERSION = process.env.API_VERSION || 'v1';

// API endpoints
export const ENDPOINTS = {
  CHATS: `/api/${API_VERSION}/chats`,
  MESSAGES: `/api/${API_VERSION}/chats/messages`,
}; 