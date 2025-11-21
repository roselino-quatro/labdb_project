'use client';

import { useState, useEffect, FormEvent, Suspense } from 'react';
import { useSearchParams, useRouter } from 'next/navigation';
import Layout from '@/components/Layout';
import ProtectedRoute from '@/components/ProtectedRoute';
import { apiGet } from '@/lib/api';

interface Reservation {
  nome_instalacao: string;
  data_reserva: string;
  horario_inicio: string;
  horario_fim: string;
}

interface AvailableInstallation {
  nome: string;
  tipo: string;
  capacidade: number;
}

function InternalDashboardContent() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const [reservas, setReservas] = useState<Reservation[]>([]);
  const [availableInstalls, setAvailableInstalls] = useState<AvailableInstallation[]>([]);
  const [filters, setFilters] = useState({
    cpf: searchParams.get('cpf') || '',
    date: searchParams.get('date') || '',
    start: searchParams.get('start') || '',
    end: searchParams.get('end') || '',
  });
  const [loading, setLoading] = useState(false);

  const loadDashboardData = async () => {
    setLoading(true);
    try {
      const params = new URLSearchParams();
      if (filters.cpf) params.append('cpf', filters.cpf);
      if (filters.date) params.append('date', filters.date);
      if (filters.start) params.append('start', filters.start);
      if (filters.end) params.append('end', filters.end);

      const data = await apiGet<{
        success: boolean;
        reservas: Reservation[];
        available_installs: AvailableInstallation[];
      }>(`/internal/?${params.toString()}`);

      if (data.success) {
        setReservas(data.reservas || []);
        setAvailableInstalls(data.available_installs || []);
      }
    } catch (err) {
      console.error('Erro ao carregar dados:', err);
      setReservas([]);
      setAvailableInstalls([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadDashboardData();
  }, [searchParams]);

  const handleCpfSubmit = (e: FormEvent) => {
    e.preventDefault();
    const params = new URLSearchParams();
    if (filters.cpf) params.append('cpf', filters.cpf);
    if (filters.date) params.append('date', filters.date);
    if (filters.start) params.append('start', filters.start);
    if (filters.end) params.append('end', filters.end);
    router.push(`/internal/dashboard?${params.toString()}`);
  };

  const handleAvailabilitySubmit = (e: FormEvent) => {
    e.preventDefault();
    const params = new URLSearchParams();
    if (filters.cpf) params.append('cpf', filters.cpf);
    if (filters.date) params.append('date', filters.date);
    if (filters.start) params.append('start', filters.start);
    if (filters.end) params.append('end', filters.end);
    router.push(`/internal/dashboard?${params.toString()}`);
  };

  return (
    <Layout>
      <section className="space-y-6">
        <header>
          <h1 className="text-2xl font-semibold text-gray-900">Área do Membro Interno</h1>
        </header>

        <div className="grid gap-6 lg:grid-cols-2">
          <form onSubmit={handleCpfSubmit} className="rounded-lg bg-white p-4 shadow">
            <h2 className="text-lg font-semibold text-gray-900">Reservas por CPF</h2>
            <label className="mt-4 block text-sm text-gray-600">
              <span className="mb-1 block font-medium">CPF</span>
              <input
                type="text"
                name="cpf"
                value={filters.cpf}
                onChange={(e) => setFilters({ ...filters, cpf: e.target.value })}
                placeholder="Apenas números"
                className="w-full rounded border border-gray-300 px-3 py-2 focus:border-[#1094ab] focus:outline-none focus:ring-1 focus:ring-[#1094ab]"
              />
            </label>
            <input type="hidden" name="date" value={filters.date} />
            <input type="hidden" name="start" value={filters.start} />
            <input type="hidden" name="end" value={filters.end} />
            <div className="mt-4 flex justify-end gap-2">
              <button
                type="button"
                onClick={() => {
                  setFilters({ cpf: '', date: '', start: '', end: '' });
                  router.push('/internal/dashboard');
                }}
                className="rounded border border-gray-300 px-4 py-2 text-sm font-semibold text-gray-600 hover:bg-gray-50"
              >
                Limpar
              </button>
              <button
                type="submit"
                className="rounded bg-[#1094ab] px-4 py-2 text-sm font-semibold text-white hover:bg-[#64c4d2] hover:text-[#1094ab]"
              >
                Carregar dados
              </button>
            </div>
          </form>

          <form onSubmit={handleAvailabilitySubmit} className="rounded-lg bg-white p-4 shadow">
            <h2 className="text-lg font-semibold text-gray-900">Instalações disponíveis</h2>
            <input type="hidden" name="cpf" value={filters.cpf} />
            <div className="mt-4 grid gap-4 sm:grid-cols-3">
              <label className="text-sm text-gray-600">
                <span className="mb-1 block font-medium">Data</span>
                <input
                  type="date"
                  name="date"
                  value={filters.date}
                  onChange={(e) => setFilters({ ...filters, date: e.target.value })}
                  className="w-full rounded border border-gray-300 px-3 py-2 focus:border-[#1094ab] focus:outline-none focus:ring-1 focus:ring-[#1094ab]"
                />
              </label>
              <label className="text-sm text-gray-600">
                <span className="mb-1 block font-medium">Início</span>
                <input
                  type="time"
                  name="start"
                  value={filters.start}
                  onChange={(e) => setFilters({ ...filters, start: e.target.value })}
                  className="w-full rounded border border-gray-300 px-3 py-2 focus:border-[#1094ab] focus:outline-none focus:ring-1 focus:ring-[#1094ab]"
                />
              </label>
              <label className="text-sm text-gray-600">
                <span className="mb-1 block font-medium">Fim</span>
                <input
                  type="time"
                  name="end"
                  value={filters.end}
                  onChange={(e) => setFilters({ ...filters, end: e.target.value })}
                  className="w-full rounded border border-gray-300 px-3 py-2 focus:border-[#1094ab] focus:outline-none focus:ring-1 focus:ring-[#1094ab]"
                />
              </label>
            </div>
            <div className="mt-4 flex justify-end gap-2">
              <button
                type="button"
                onClick={() => {
                  setFilters({ cpf: '', date: '', start: '', end: '' });
                  router.push('/internal/dashboard');
                }}
                className="rounded border border-gray-300 px-4 py-2 text-sm font-semibold text-gray-600 hover:bg-gray-50"
              >
                Limpar
              </button>
              <button
                type="submit"
                className="rounded bg-[#1094ab] px-4 py-2 text-sm font-semibold text-white hover:bg-[#64c4d2] hover:text-[#1094ab]"
              >
                Verificar disponibilidade
              </button>
            </div>
          </form>
        </div>

        <div className="grid gap-6 lg:grid-cols-2">
          <div className="rounded-lg bg-white p-4 shadow">
            <h3 className="text-lg font-semibold text-gray-900">Reservas registradas</h3>
            <div className="mt-4 overflow-x-auto">
              <table className="min-w-full text-sm">
                <thead className="border-b text-left text-gray-500">
                  <tr>
                    <th className="px-3 py-2">Instalação</th>
                    <th className="px-3 py-2">Data</th>
                    <th className="px-3 py-2">Horário</th>
                  </tr>
                </thead>
                <tbody className="divide-y">
                  {reservas.length > 0 ? (
                    reservas.map((reserva, index) => (
                      <tr key={index}>
                        <td className="px-3 py-2 font-medium text-gray-900">{reserva.nome_instalacao}</td>
                        <td className="px-3 py-2">{reserva.data_reserva}</td>
                        <td className="px-3 py-2">
                          {reserva.horario_inicio} - {reserva.horario_fim}
                        </td>
                      </tr>
                    ))
                  ) : (
                    <tr>
                      <td className="px-3 py-4 text-gray-500" colSpan={3}>
                        {filters.cpf ? 'Nenhuma reserva foi retornada para o CPF informado.' : 'Nenhuma reserva agendada.'}
                      </td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
          </div>

          <div className="rounded-lg bg-white p-4 shadow">
            <h3 className="text-lg font-semibold text-gray-900">Instalações disponíveis</h3>
            <div className="mt-4 overflow-x-auto">
              <table className="min-w-full text-sm">
                <thead className="border-b text-left text-gray-500">
                  <tr>
                    <th className="px-3 py-2">Instalação</th>
                    <th className="px-3 py-2">Tipo</th>
                    <th className="px-3 py-2">Capacidade</th>
                  </tr>
                </thead>
                <tbody className="divide-y">
                  {availableInstalls.length > 0 ? (
                    availableInstalls.map((item, index) => (
                      <tr key={index}>
                        <td className="px-3 py-2 font-medium text-gray-900">{item.nome}</td>
                        <td className="px-3 py-2">{item.tipo}</td>
                        <td className="px-3 py-2">{item.capacidade}</td>
                      </tr>
                    ))
                  ) : (
                    <tr>
                      <td className="px-3 py-4 text-gray-500" colSpan={3}>
                        {filters.date && filters.start && filters.end ? 'Nenhuma instalação disponível no período selecionado.' : 'Selecione data e horário para ver disponibilidade.'}
                      </td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </section>
    </Layout>
  );
}

export default function InternalDashboardPage() {
  return (
    <ProtectedRoute allowedRoles={['internal', 'staff', 'admin']}>
      <Suspense fallback={<div>Carregando...</div>}>
        <InternalDashboardContent />
      </Suspense>
    </ProtectedRoute>
  );
}
