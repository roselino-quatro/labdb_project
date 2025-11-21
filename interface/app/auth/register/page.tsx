'use client';

import { useState, FormEvent } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import Layout from '@/components/Layout';

export default function RegisterPage() {
  const router = useRouter();
  const [formData, setFormData] = useState({
    cpf: '',
    nusp: '',
    email: '',
    password: '',
    password_confirm: '',
  });
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setError('');
    setSuccess('');

    if (formData.password !== formData.password_confirm) {
      setError('As senhas não coincidem');
      return;
    }

    setLoading(true);

    try {
      const data = new FormData();
      data.append('cpf', formData.cpf);
      data.append('nusp', formData.nusp);
      data.append('email', formData.email);
      data.append('password', formData.password);
      data.append('password_confirm', formData.password_confirm);

      const response = await fetch('http://localhost:5050/auth/register', {
        method: 'POST',
        body: data,
        credentials: 'include',
      });

      if (response.ok) {
        setSuccess('Solicitação de cadastro criada com sucesso');
        setTimeout(() => {
          router.push('/auth/login');
        }, 2000);
      } else {
        const result = await response.json().catch(() => ({ message: 'Erro ao processar solicitação' }));
        setError(result.message || 'Erro ao processar solicitação');
      }
    } catch (err) {
      setError('Erro ao processar solicitação. Tente novamente.');
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
          <h1 className="mt-4 text-2xl font-bold text-gray-900">Solicitar Cadastro</h1>
          <p className="mt-2 text-sm text-gray-500">
            Apenas internos USP podem solicitar cadastro. Aguarde aprovação do administrador.
          </p>
        </div>
        {error && (
          <div className="mb-4 rounded-lg bg-red-50 p-3 text-sm text-red-800">
            {error}
          </div>
        )}
        {success && (
          <div className="mb-4 rounded-lg bg-green-50 p-3 text-sm text-green-800">
            {success}
          </div>
        )}
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label htmlFor="cpf" className="mb-1 block text-sm font-medium text-gray-700">
              CPF
            </label>
            <input
              id="cpf"
              name="cpf"
              type="text"
              required
              pattern="[0-9]{11}"
              maxLength={11}
              value={formData.cpf}
              onChange={(e) => setFormData({ ...formData, cpf: e.target.value })}
              className="w-full rounded border border-gray-300 px-4 py-2 text-sm shadow-sm focus:border-[#1094ab] focus:outline-none focus:ring-1 focus:ring-[#1094ab]"
              placeholder="00000000000"
            />
          </div>
          <div>
            <label htmlFor="nusp" className="mb-1 block text-sm font-medium text-gray-700">
              NUSP
            </label>
            <input
              id="nusp"
              name="nusp"
              type="text"
              required
              pattern="[0-9]{5,8}"
              maxLength={8}
              value={formData.nusp}
              onChange={(e) => setFormData({ ...formData, nusp: e.target.value })}
              className="w-full rounded border border-gray-300 px-4 py-2 text-sm shadow-sm focus:border-[#1094ab] focus:outline-none focus:ring-1 focus:ring-[#1094ab]"
              placeholder="00000"
            />
          </div>
          <div>
            <label htmlFor="email" className="mb-1 block text-sm font-medium text-gray-700">
              E-mail institucional
            </label>
            <input
              id="email"
              name="email"
              type="email"
              required
              value={formData.email}
              onChange={(e) => setFormData({ ...formData, email: e.target.value })}
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
              minLength={6}
              value={formData.password}
              onChange={(e) => setFormData({ ...formData, password: e.target.value })}
              className="w-full rounded border border-gray-300 px-4 py-2 text-sm shadow-sm focus:border-[#1094ab] focus:outline-none focus:ring-1 focus:ring-[#1094ab]"
              placeholder="Digite sua senha"
            />
          </div>
          <div>
            <label htmlFor="password_confirm" className="mb-1 block text-sm font-medium text-gray-700">
              Confirmar Senha
            </label>
            <input
              id="password_confirm"
              name="password_confirm"
              type="password"
              required
              minLength={6}
              value={formData.password_confirm}
              onChange={(e) => setFormData({ ...formData, password_confirm: e.target.value })}
              className="w-full rounded border border-gray-300 px-4 py-2 text-sm shadow-sm focus:border-[#1094ab] focus:outline-none focus:ring-1 focus:ring-[#1094ab]"
              placeholder="Confirme sua senha"
            />
          </div>
          <button
            type="submit"
            disabled={loading}
            className="w-full rounded bg-[#1094ab] px-4 py-2 text-sm font-semibold text-white transition hover:bg-[#64c4d2] hover:text-[#1094ab] disabled:opacity-50"
          >
            {loading ? 'Enviando...' : 'Solicitar Cadastro'}
          </button>
        </form>
        <div className="mt-6 text-center text-sm">
          <Link href="/auth/login" className="text-[#1094ab] hover:text-[#fcb421]">
            Já tem uma conta? Faça login
          </Link>
        </div>
      </div>
    </Layout>
  );
}
