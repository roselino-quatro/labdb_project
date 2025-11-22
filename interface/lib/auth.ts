import { apiGet } from "@/lib/api";

export interface User {
  user_id: string;
  email: string;
  nome: string;
  roles: {
    admin?: boolean;
    staff?: boolean;
    internal?: boolean;
    external?: boolean;
  };
}

export interface AuthResponse {
  success: boolean;
  user?: User;
  message?: string;
}

let currentUserCache: User | null = null;
let userCachePromise: Promise<User | null> | null = null;

/**
 * Get current user information from session.
 * Uses caching to avoid multiple API calls.
 */
export async function getCurrentUser(): Promise<User | null> {
  // Return cached user if available
  if (currentUserCache) {
    return currentUserCache;
  }

  // Return existing promise if already fetching
  if (userCachePromise) {
    return userCachePromise;
  }

  // Fetch user data
  userCachePromise = (async () => {
    try {
      const response = await apiGet<AuthResponse>("/auth/me");
      if (response.success && response.user) {
        currentUserCache = response.user;
        return response.user;
      }
      return null;
    } catch (error) {
      console.error("Error fetching current user:", error);
      return null;
    } finally {
      userCachePromise = null;
    }
  })();

  return userCachePromise;
}

/**
 * Clear the user cache (useful after logout).
 */
export function clearUserCache(): void {
  currentUserCache = null;
  userCachePromise = null;
}

/**
 * Check if user has a specific role.
 */
export function hasRole(
  user: User | null,
  role: "admin" | "staff" | "internal" | "external"
): boolean {
  if (!user || !user.roles) {
    return false;
  }
  return user.roles[role] === true;
}

/**
 * Check if user has any of the specified roles.
 */
export function hasAnyRole(
  user: User | null,
  roles: Array<"admin" | "staff" | "internal" | "external">
): boolean {
  if (!user || !user.roles) {
    return false;
  }
  return roles.some((role) => user.roles[role] === true);
}

/**
 * Check if user is authenticated.
 */
export function isAuthenticated(user: User | null): boolean {
  return user !== null && user.user_id !== undefined;
}
