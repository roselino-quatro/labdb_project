'use client';

import Link from 'next/link';

export default function Navbar() {
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
          <Link href="/admin/dashboard" className="hover:text-[#1094ab]">
            Administração
          </Link>
          <Link href="/reports/overview" className="hover:text-[#1094ab]">
            Relatórios
          </Link>
          <Link href="/staff/dashboard" className="hover:text-[#1094ab]">
            Equipe
          </Link>
          <Link href="/internal/dashboard" className="hover:text-[#1094ab]">
            Interno
          </Link>
          <Link href="/external/dashboard" className="hover:text-[#1094ab]">
            Externo
          </Link>
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
