'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import { getCurrentUser, User, hasRole } from '@/lib/auth';

export default function Navbar() {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadUser() {
      try {
        const currentUser = await getCurrentUser();
        setUser(currentUser);
      } catch (error) {
        console.error('Error loading user:', error);
      } finally {
        setLoading(false);
      }
    }

    loadUser();
  }, []);

  // Don't show navbar if not authenticated
  if (loading || !user) {
    return null;
  }

  const showAdmin = hasRole(user, 'admin');
  const showStaff = hasRole(user, 'staff') || hasRole(user, 'admin');
  const showInternal = hasRole(user, 'internal') || hasRole(user, 'staff') || hasRole(user, 'admin');
  const showExternal = hasRole(user, 'external') || hasRole(user, 'admin');
  const showReports = hasRole(user, 'admin') || hasRole(user, 'staff'); // Ajustar conforme necessário

  return (
    <header className="bg-white shadow">
      <div className="container mx-auto flex flex-wrap items-center justify-between gap-4 px-6 py-4">
        <div className="flex items-center space-x-3">
          <span className="inline-flex h-10 w-10 items-center justify-center rounded-full bg-[#1094ab] text-white font-semibold">
            CE
          </span>
          <div className="text-lg font-semibold text-gray-800">CEFER</div>
        </div>
        <nav className="flex flex-wrap items-center gap-4 text-sm font-medium text-gray-600">
          {showAdmin && (
            <Link href="/admin/dashboard" className="hover:text-[#1094ab]">
              Administração
            </Link>
          )}
          {showReports && (
            <Link href="/reports/overview" className="hover:text-[#1094ab]">
              Relatórios
            </Link>
          )}
          {showStaff && (
            <Link href="/staff/dashboard" className="hover:text-[#1094ab]">
              Equipe
            </Link>
          )}
          {showInternal && (
            <Link href="/internal/dashboard" className="hover:text-[#1094ab]">
              Interno
            </Link>
          )}
          {showExternal && (
            <Link href="/external/dashboard" className="hover:text-[#1094ab]">
              Externo
            </Link>
          )}
        </nav>
        <Link
          href="/auth/logout"
          className="rounded bg-[#1094ab] px-4 py-2 text-sm font-semibold text-white hover:bg-[#64c4d2] hover:text-[#1094ab]"
        >
          Sair
        </Link>
      </div>
    </header>
  );
}
