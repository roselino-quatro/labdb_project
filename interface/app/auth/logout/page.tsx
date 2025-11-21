'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { clearUserCache } from '@/lib/auth';
import { apiGet } from '@/lib/api';

export default function LogoutPage() {
  const router = useRouter();

  useEffect(() => {
    const logout = async () => {
      try {
        await apiGet('/auth/logout');
      } catch (err) {
        console.error('Erro ao fazer logout:', err);
      } finally {
        clearUserCache();
        router.push('/auth/login');
      }
    };

    logout();
  }, [router]);

  return (
    <div className="flex min-h-screen items-center justify-center">
      <p>Saindo...</p>
    </div>
  );
}
