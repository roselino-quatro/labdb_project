'use client';

import { useState, useEffect, FormEvent, Suspense } from 'react';
import { useSearchParams, useRouter } from 'next/navigation';
import Layout from '@/components/Layout';
import ProtectedRoute from '@/components/ProtectedRoute';
import { apiGet } from '@/lib/api';

interface Activity {
  nome_atividade: string;
  grupo_extensao: string | null;
  weekday: string;
  horario_inicio: string;
  horario_fim: string;
  vagas_ocupadas: number;
  vagas_limite: number;
}

function StaffDashboardContent() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const [activities, setActivities] = useState<Activity[]>([]);
  const [filters, setFilters] = useState({
    weekday: searchParams.get('weekday') || '',
    group: searchParams.get('group') || '',
    modality: searchParams.get('modality') || '',
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadActivities();
  }, [searchParams]);

  const loadActivities = async () => {
    try {
      const params = new URLSearchParams();
      if (filters.weekday) params.append('weekday', filters.weekday);
      if (filters.group) params.append('group', filters.group);
      if (filters.modality) params.append('modality', filters.modality);

      const data = await apiGet<{
        success: boolean;
        activities: Activity[];
      }>(`/staff/?${params.toString()}`);

      if (data.success) {
        setActivities(data.activities || []);
      }
    } catch (err) {
      console.error('Erro ao carregar atividades:', err);
      setActivities([]);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    const params = new URLSearchParams();
    if (filters.weekday) params.append('weekday', filters.weekday);
    if (filters.group) params.append('group', filters.group);
    if (filters.modality) params.append('modality', filters.modality);
    router.push(`/staff/dashboard?${params.toString()}`);
  };

  return (
    <Layout>
      <section className="space-y-6">
        <header>
          <h1 className="text-2xl font-semibold text-gray-900">Painel de Atividades da Equipe</h1>
        </header>

        <form onSubmit={handleSubmit} className="grid gap-4 rounded-lg bg-white p-4 shadow sm:grid-cols-3">
          <label className="text-sm text-gray-600">
            <span className="mb-1 block font-medium">Dia da semana</span>
            <select
              name="weekday"
              value={filters.weekday}
              onChange={(e) => setFilters({ ...filters, weekday: e.target.value })}
              className="w-full rounded border border-gray-300 px-3 py-2 focus:border-[#1094ab] focus:outline-none focus:ring-1 focus:ring-[#1094ab]"
            >
              <option value="">Todos os dias</option>
              <option value="SEGUNDA">Segunda-feira</option>
              <option value="TERCA">Terça-feira</option>
              <option value="QUARTA">Quarta-feira</option>
              <option value="QUINTA">Quinta-feira</option>
              <option value="SEXTA">Sexta-feira</option>
              <option value="SABADO">Sábado</option>
              <option value="DOMINGO">Domingo</option>
            </select>
          </label>
          <label className="text-sm text-gray-600">
            <span className="mb-1 block font-medium">Grupo de extensão</span>
            <input
              type="text"
              name="group"
              value={filters.group}
              onChange={(e) => setFilters({ ...filters, group: e.target.value })}
              placeholder="Nome do grupo"
              className="w-full rounded border border-gray-300 px-3 py-2 focus:border-[#1094ab] focus:outline-none focus:ring-1 focus:ring-[#1094ab]"
            />
          </label>
          <label className="text-sm text-gray-600">
            <span className="mb-1 block font-medium">Modalidade</span>
            <input
              type="text"
              name="modality"
              value={filters.modality}
              onChange={(e) => setFilters({ ...filters, modality: e.target.value })}
              placeholder="Nome da atividade"
              className="w-full rounded border border-gray-300 px-3 py-2 focus:border-[#1094ab] focus:outline-none focus:ring-1 focus:ring-[#1094ab]"
            />
          </label>
          <div className="sm:col-span-3 flex justify-end gap-2">
            <button
              type="button"
              onClick={() => {
                setFilters({ weekday: '', group: '', modality: '' });
                router.push('/staff/dashboard');
              }}
              className="rounded border border-gray-300 px-4 py-2 text-sm font-semibold text-gray-600 hover:bg-gray-50"
            >
              Limpar
            </button>
            <button
              type="submit"
              className="rounded bg-[#1094ab] px-4 py-2 text-sm font-semibold text-white hover:bg-[#64c4d2] hover:text-[#1094ab]"
            >
              Aplicar filtros
            </button>
          </div>
        </form>

        <div className="overflow-x-auto rounded-lg bg-white shadow">
          <table className="min-w-full text-sm">
            <thead className="border-b text-left text-gray-500">
              <tr>
                <th className="px-4 py-3">Atividade</th>
                <th className="px-4 py-3">Grupo</th>
                <th className="px-4 py-3">Dia da semana</th>
                <th className="px-4 py-3">Horário</th>
                <th className="px-4 py-3">Inscrições</th>
              </tr>
            </thead>
            <tbody className="divide-y">
              {activities.length > 0 ? (
                activities.map((activity, index) => (
                  <tr key={index}>
                    <td className="px-4 py-3 font-medium text-gray-900">{activity.nome_atividade}</td>
                    <td className="px-4 py-3">{activity.grupo_extensao || '—'}</td>
                    <td className="px-4 py-3">{activity.weekday}</td>
                    <td className="px-4 py-3">
                      {activity.horario_inicio} - {activity.horario_fim}
                    </td>
                    <td className="px-4 py-3">
                      {activity.vagas_ocupadas} / {activity.vagas_limite}
                    </td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td className="px-4 py-6 text-center text-gray-500" colSpan={5}>
                    Nenhuma atividade corresponde aos filtros selecionados.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </section>
    </Layout>
  );
}

export default function StaffDashboardPage() {
  return (
    <ProtectedRoute allowedRoles={['staff', 'admin']}>
      <Suspense fallback={<div>Carregando...</div>}>
        <StaffDashboardContent />
      </Suspense>
    </ProtectedRoute>
  );
}
