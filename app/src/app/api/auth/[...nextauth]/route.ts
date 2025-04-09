import NextAuth, { DefaultSession } from 'next-auth';
import CredentialsProvider from 'next-auth/providers/credentials';
import GoogleProvider from 'next-auth/providers/google';
import GithubProvider from 'next-auth/providers/github';
import { JWT } from 'next-auth/jwt';
import { env } from '@/env';

// Define user interface
interface UserDetails {
  id: string;
  email: string;
  username: string;
  phone_number: string | null;
  profile_picture_url: string | null;
  is_active: boolean;
  is_verified: boolean;
  last_login_at: string;
  created_at: string;
  updated_at: string;
}

// Extend the built-in session type
declare module 'next-auth' {
  interface Session extends DefaultSession {
    accessToken?: string;
    refreshToken?: string;
    userId?: string;
    user: DefaultSession["user"] & Partial<UserDetails>;
  }
  interface User {
    accessToken?: string;
    refreshToken?: string;
    id: string;
    username?: string;
    profile_picture_url?: string | null;
    is_verified?: boolean;
  }
}

declare module 'next-auth/jwt' {
  interface JWT {
    accessToken?: string;
    refreshToken?: string;
    userId?: string;
    username?: string;
    profile_picture_url?: string | null;
    is_verified?: boolean;
    userDetails?: UserDetails;
  }
}

const handler = NextAuth({
  providers: [
    GoogleProvider({
      clientId: env.GOOGLE_CLIENT_ID,
      clientSecret: env.GOOGLE_CLIENT_SECRET,
    }),
    GithubProvider({
      clientId: env.GITHUB_ID,
      clientSecret: env.GITHUB_SECRET,
    }),
    CredentialsProvider({
      name: 'credentials',
      credentials: {
        email: { label: 'Email', type: 'email' },
        password: { label: 'Password', type: 'password' },
      },
      async authorize(credentials) {
        try {
          if (!credentials?.email || !credentials?.password) {
            throw new Error('Email and password required');
          }

          const response = await fetch(`${env.NEXT_PUBLIC_API_URL}/api/v1/login`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              email: credentials.email,
              password: credentials.password,
            }),
          });

          const data = await response.json();

          if (!response.ok || data.error) {
            throw new Error(data.error || 'Invalid credentials');
          }

          // Extract tokens from the response data
          const { access_token, refresh_token } = data.data;
          
          // Check if tokens exist
          if (!access_token || !refresh_token) {
            throw new Error('Authentication tokens not found in response');
          }

          // Parse the JWT to get the user ID
          const tokenParts = access_token.split('.');
          const payload = JSON.parse(Buffer.from(tokenParts[1], 'base64').toString());
          const userId = payload.id;

          // Return the user object that will be saved in the session
          return {
            id: userId,
            email: credentials.email,
            accessToken: access_token,
            refreshToken: refresh_token,
          };
        } catch (error) {
          throw new Error(error instanceof Error ? error.message : 'Invalid credentials');
        }
      },
    }),
  ],
  pages: {
    signIn: '/login',
  },
  callbacks: {
    async jwt({ token, user }) {
      if (user) {
        // Add auth tokens to the JWT token
        token.accessToken = user.accessToken;
        token.refreshToken = user.refreshToken;
        token.userId = user.id;
        
        // Fetch user data if we have an access token
        if (user.accessToken) {
          try {
            const meResponse = await fetch(`${env.NEXT_PUBLIC_API_URL}/api/v1/me`, {
              method: 'GET',
              headers: {
                'Authorization': `Bearer ${user.accessToken}`,
              },
            });
            
            const userData = await meResponse.json();
            
            if (meResponse.ok && !userData.error) {
              // Save user data to token
              token.userDetails = userData.data;
              token.username = userData.data.username;
              token.profile_picture_url = userData.data.profile_picture_url;
              token.is_verified = userData.data.is_verified;
            } else {
              console.error('Failed to fetch user data:', userData.error);
            }
          } catch (error) {
            console.error('Error fetching user details:', error);
          }
        }
      }
      return token;
    },
    async session({ session, token }) {
      // Add auth tokens to the session
      if (token) {
        session.accessToken = token.accessToken;
        session.refreshToken = token.refreshToken;
        session.userId = token.userId;
        
        // Add user details to session
        if (token.userDetails) {
          session.user = {
            ...session.user,
            ...token.userDetails,
          };
        }
        
        // Add specific user properties for easier access
        if (session.user) {
          session.user.name = token.username || session.user.name;
          session.user.image = token.profile_picture_url || session.user.image;
        }
      }
      return session;
    },
  },
  events: {
    async signOut({ token }) {
      if (token?.refreshToken) {
        try {
          // Call the logout API with the refresh token
          const response = await fetch(`${env.NEXT_PUBLIC_API_URL}/api/v1/logout`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'Refresh-Token': token.refreshToken as string,
            },
          });
          
          if (!response.ok) {
            console.error('Failed to logout from API:', await response.text());
          }
        } catch (error) {
          console.error('Error during logout:', error);
        }
      }
    },
  },
  session: {
    strategy: 'jwt',
  },
});

export { handler as GET, handler as POST };
