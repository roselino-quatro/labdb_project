'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { getCurrentUser, hasAnyRole, User } from '@/lib/auth';

interface ProtectedRouteProps {
  children: React.ReactNode;
  allowedRoles: Array<'admin' | 'staff' | 'internal' | 'external'>;
  redirectTo?: string;
}

export default function ProtectedRoute({
  children,
  allowedRoles,
  redirectTo,
}: ProtectedRouteProps) {
  const router = useRouter();
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [authorized, setAuthorized] = useState(false);

  useEffect(() => {
    async function checkAuth() {
      try {
        const currentUser = await getCurrentUser();
        setUser(currentUser);

        if (!currentUser) {
          // Not authenticated, redirect to appropriate login
          if (allowedRoles.includes('external')) {
            router.push('/auth/login/external');
          } else {
            router.push('/auth/login');
          }
          return;
        }

        // Check if user has required role
        // For external users, check if they have external role OR if they're authenticated via token
        const hasAccess = hasAnyRole(currentUser, allowedRoles);
        setAuthorized(hasAccess);

        if (!hasAccess) {
          // User doesn't have required role, redirect to their dashboard
          if (currentUser.roles.admin) {
            router.push('/admin/dashboard');
          } else if (currentUser.roles.staff) {
            router.push('/staff/dashboard');
          } else if (currentUser.roles.internal) {
            router.push('/internal/dashboard');
          } else if (currentUser.roles.external) {
            router.push('/external/dashboard');
          } else {
            router.push(redirectTo || '/auth/login');
          }
        }
      } catch (error) {
        console.error('Error checking authentication:', error);
        // If external role is allowed, try external login first
        if (allowedRoles.includes('external')) {
          router.push('/auth/login/external');
        } else {
          router.push('/auth/login');
        }
      } finally {
        setLoading(false);
      }
    }

    checkAuth();
  }, [router, allowedRoles, redirectTo]);

  if (loading) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <div className="text-center">
          <div className="mb-4 inline-block h-8 w-8 animate-spin rounded-full border-4 border-solid border-[#1094ab] border-r-transparent"></div>
          <p className="text-sm text-gray-600">Verificando permissões...</p>
        </div>
      </div>
    );
  }

  if (!authorized) {
    return null;
  }

  return <>{children}</>;
}
