'use client';

import { useState, FormEvent } from 'react';
import { useRouter } from 'next/navigation';
import Layout from '@/components/Layout';
import { apiPost } from '@/lib/api';

export default function LoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const formData = new FormData();
      formData.append('email', email);
      formData.append('password', password);

      const response = await fetch('http://localhost:5050/auth/login', {
        method: 'POST',
        body: formData,
        credentials: 'include',
      });

      if (response.ok) {
        router.push('/admin/dashboard');
      } else {
        const data = await response.json().catch(() => ({ message: 'Credenciais inválidas' }));
        setError(data.message || 'Credenciais inválidas');
      }
    } catch (err) {
      setError('Erro ao fazer login. Tente novamente.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Layout hideNavbar hideFooter hideDebugButtons mainClass="flex min-h-screen items-center justify-center bg-gradient-to-br from-[#1094ab] to-[#64c4d2] p-6">
      <div className="w-full max-w-md rounded-lg bg-white p-8 shadow-xl">
        <div className="mb-6 text-center">
          <span className="inline-flex h-12 w-12 items-center justify-center rounded-full bg-[#1094ab] text-xl font-bold text-white">
            CE
          </span>
          <h1 className="mt-4 text-2xl font-bold text-gray-900">Acesse o Sistema CEFER</h1>
          <p className="mt-2 text-sm text-gray-500">
            Gerencie atividades, reservas e usuários com segurança.
          </p>
        </div>
        {error && (
          <div className="mb-4 rounded-lg bg-red-50 p-3 text-sm text-red-800">
            {error}
          </div>
        )}
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label htmlFor="email" className="mb-1 block text-sm font-medium text-gray-700">
              E-mail institucional
            </label>
            <input
              id="email"
              name="email"
              type="email"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full rounded border border-gray-300 px-4 py-2 text-sm shadow-sm focus:border-[#1094ab] focus:outline-none focus:ring-1 focus:ring-[#1094ab]"
              placeholder="nome.sobrenome@usp.br"
            />
          </div>
          <div>
            <label htmlFor="password" className="mb-1 block text-sm font-medium text-gray-700">
              Senha
            </label>
            <input
              id="password"
              name="password"
              type="password"
              required
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full rounded border border-gray-300 px-4 py-2 text-sm shadow-sm focus:border-[#1094ab] focus:outline-none focus:ring-1 focus:ring-[#1094ab]"
              placeholder="Digite sua senha"
            />
          </div>
          <button
            type="submit"
            disabled={loading}
            className="w-full rounded bg-[#1094ab] px-4 py-2 text-sm font-semibold text-white transition hover:bg-[#64c4d2] hover:text-[#1094ab] disabled:opacity-50"
          >
            {loading ? 'Entrando...' : 'Entrar'}
          </button>
        </form>
        <div className="mt-6 rounded-lg bg-gray-50 p-4 text-sm text-gray-600">
          <h2 className="mb-2 font-semibold text-gray-800">Perfis com acesso</h2>
          <ul className="space-y-1">
            <li>Administrador: gerenciamento completo do CEFER.</li>
            <li>Funcionário CEFER: administração de atividades e instalações.</li>
            <li>Interno USP: reservas, inscrições e convites.</li>
            <li>Externo USP: acesso mediante convite validado.</li>
          </ul>
        </div>
      </div>
    </Layout>
  );
}
