'use server';

import { env } from '@/env';

interface RegisterRequest {
  email: string;
  username: string;
  password: string;
}

interface AuthResponse {
  token?: string;
  error?: string;
}

export async function register(data: RegisterRequest): Promise<AuthResponse> {
  try {
    const response = await fetch(`${env.NEXT_PUBLIC_API_URL}/api/v1/register`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });

    const result = await response.json();

    if (!response.ok) {
      throw new Error(result.error || 'Registration failed');
    }

    return result;
  } catch (error) {
    return {
      error: error instanceof Error ? error.message : 'An error occurred during registration',
    };
  }
}
