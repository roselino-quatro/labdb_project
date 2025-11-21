'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import Layout from '@/components/Layout';
import { apiGet, apiPost } from '@/lib/api';

interface Registration {
  id_solicitacao: number;
  cpf_pessoa: string;
  nome: string;
  email: string;
  nusp: string;
  data_solicitacao: string;
}

export default function PendingRegistrationsPage() {
  const router = useRouter();
  const [registrations, setRegistrations] = useState<Registration[]>([]);
  const [loading, setLoading] = useState(true);
  const [message, setMessage] = useState<{ category: 'success' | 'error'; text: string } | null>(null);

  useEffect(() => {
    loadRegistrations();
  }, []);

  const loadRegistrations = async () => {
    try {
      const data = await apiGet<{
        success: boolean;
        registrations: Registration[];
      }>('/auth/pending-registrations');

      if (data.success && Array.isArray(data.registrations)) {
        setRegistrations(data.registrations);
      } else {
        setRegistrations([]);
      }
    } catch (err) {
      console.error('Erro ao carregar registrations:', err);
      setRegistrations([]);
    } finally {
      setLoading(false);
    }
  };

  const handleApprove = async (id: number) => {
    try {
      const data = await apiPost<{
        success: boolean;
        message?: string;
      }>('/auth/approve-registration', {
        id_solicitacao: id,
      });

      if (data.success) {
        setMessage({ category: 'success', text: data.message || 'Cadastro aprovado com sucesso' });
        loadRegistrations();
      } else {
        setMessage({ category: 'error', text: data.message || 'Erro ao aprovar cadastro' });
      }
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Erro ao processar solicitação';
      try {
        const errorData = JSON.parse(errorMessage);
        setMessage({ category: 'error', text: errorData.message || 'Erro ao aprovar cadastro' });
      } catch {
        setMessage({ category: 'error', text: errorMessage });
      }
    }
  };

  const handleReject = async (id: number) => {
    if (!confirm('Tem certeza que deseja rejeitar esta solicitação?')) {
      return;
    }

    try {
      const data = await apiPost<{
        success: boolean;
        message?: string;
      }>('/auth/reject-registration', {
        id_solicitacao: id,
        observacoes: '',
      });

      if (data.success) {
        setMessage({ category: 'success', text: data.message || 'Cadastro rejeitado' });
        loadRegistrations();
      } else {
        setMessage({ category: 'error', text: data.message || 'Erro ao rejeitar cadastro' });
      }
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Erro ao processar solicitação';
      try {
        const errorData = JSON.parse(errorMessage);
        setMessage({ category: 'error', text: errorData.message || 'Erro ao rejeitar cadastro' });
      } catch {
        setMessage({ category: 'error', text: errorMessage });
      }
    }
  };

  const formatDate = (dateString: string) => {
    if (!dateString) return '-';
    const date = new Date(dateString);
    return date.toLocaleString('pt-BR');
  };

  return (
    <Layout messages={message ? [message] : undefined}>
      <div className="container mx-auto px-4 py-8">
        <div className="mb-6 flex items-center justify-between">
          <h1 className="text-3xl font-bold text-gray-900">Solicitações de Cadastro Pendentes</h1>
          <Link
            href="/admin/dashboard"
            className="rounded bg-gray-200 px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-300"
          >
            Voltar
          </Link>
        </div>

        {loading ? (
          <div className="text-center text-gray-500">Carregando...</div>
        ) : registrations.length > 0 ? (
          <div className="overflow-x-auto rounded-lg border border-gray-200 bg-white shadow">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500">
                    CPF
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500">
                    Nome
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500">
                    Email
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500">
                    NUSP
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500">
                    Data Solicitação
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500">
                    Ações
                  </th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200 bg-white">
                {registrations.map((reg) => (
                  <tr key={reg.id_solicitacao}>
                    <td className="whitespace-nowrap px-6 py-4 text-sm text-gray-900">{reg.cpf_pessoa}</td>
                    <td className="whitespace-nowrap px-6 py-4 text-sm text-gray-900">{reg.nome}</td>
                    <td className="whitespace-nowrap px-6 py-4 text-sm text-gray-900">{reg.email}</td>
                    <td className="whitespace-nowrap px-6 py-4 text-sm text-gray-900">{reg.nusp}</td>
                    <td className="whitespace-nowrap px-6 py-4 text-sm text-gray-900">
                      {formatDate(reg.data_solicitacao)}
                    </td>
                    <td className="whitespace-nowrap px-6 py-4 text-sm font-medium">
                      <button
                        onClick={() => handleApprove(reg.id_solicitacao)}
                        className="mr-2 rounded bg-green-600 px-3 py-1 text-white hover:bg-green-700"
                      >
                        Aprovar
                      </button>
                      <button
                        onClick={() => handleReject(reg.id_solicitacao)}
                        className="rounded bg-red-600 px-3 py-1 text-white hover:bg-red-700"
                      >
                        Rejeitar
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <div className="rounded-lg border border-gray-200 bg-white p-8 text-center shadow">
            <p className="text-gray-500">Nenhuma solicitação de cadastro pendente.</p>
          </div>
        )}
      </div>
    </Layout>
  );
}
