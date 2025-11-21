'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';

export default function LogoutPage() {
  const router = useRouter();

  useEffect(() => {
    const logout = async () => {
      try {
        await fetch('http://localhost:5050/auth/logout', {
          method: 'GET',
          credentials: 'include',
        });
      } catch (err) {
        console.error('Erro ao fazer logout:', err);
      } finally {
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
