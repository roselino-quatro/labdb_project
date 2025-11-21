'use client';

import { useState, useEffect } from 'react';
import Layout from '@/components/Layout';
import ProtectedRoute from '@/components/ProtectedRoute';
import { apiGet } from '@/lib/api';

interface Stat {
  label: string;
  value: string | number;
  description: string;
}

interface Reservation {
  installation_name: string;
  data_reserva: string;
  horario_inicio: string;
  horario_fim: string;
  responsible_name: string;
}

interface Activity {
  nome_atividade: string;
  weekday: string;
  horario_inicio: string;
  horario_fim: string;
  grupo_extensao: string | null;
  vagas_ocupadas: number;
  vagas_limite: number;
  occupancy_rate: number;
}

export default function AdminDashboardPage() {
  const [stats, setStats] = useState<Stat[]>([]);
  const [upcomingReservations, setUpcomingReservations] = useState<Reservation[]>([]);
  const [activityEnrollment, setActivityEnrollment] = useState<Activity[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      const data = await apiGet<{
        success: boolean;
        stats: Array<{ label: string; value: string | number; description: string }>;
        upcoming_reservations: Reservation[];
        activity_enrollment: Activity[];
      }>('/admin/');

      if (data.success) {
        setStats(data.stats || []);
        setUpcomingReservations(data.upcoming_reservations || []);
        setActivityEnrollment(data.activity_enrollment || []);
      }
    } catch (err) {
      console.error('Erro ao carregar dados:', err);
      setStats([]);
      setUpcomingReservations([]);
      setActivityEnrollment([]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <ProtectedRoute allowedRoles={['admin']}>
      <Layout>
        <section className="space-y-6">
          <header>
            <h1 className="text-2xl font-semibold text-gray-900">Visão Geral Administrativa</h1>
          </header>

        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          {stats.length > 0 ? (
            stats.map((stat, index) => (
              <div key={index} className="rounded-lg bg-white p-4 shadow">
                <p className="text-sm uppercase tracking-wide text-gray-500">{stat.label}</p>
                <p className="mt-2 text-3xl font-semibold text-gray-900">{stat.value}</p>
                <p className="mt-1 text-xs text-gray-500">{stat.description}</p>
              </div>
            ))
          ) : (
            <div className="rounded-lg bg-white p-4 shadow sm:col-span-2 lg:col-span-4">
              <p className="text-sm text-gray-500">Nenhuma estatística disponível.</p>
            </div>
          )}
        </div>

        <div className="grid gap-6 lg:grid-cols-2">
          <div className="rounded-lg bg-white p-4 shadow">
            <h2 className="text-lg font-semibold text-gray-900">Próximas reservas</h2>
            <div className="mt-4 overflow-x-auto">
              <table className="min-w-full text-sm">
                <thead className="border-b text-left text-gray-500">
                  <tr>
                    <th className="px-3 py-2">Instalação</th>
                    <th className="px-3 py-2">Data</th>
                    <th className="px-3 py-2">Horário</th>
                    <th className="px-3 py-2">Responsável</th>
                  </tr>
                </thead>
                <tbody className="divide-y">
                  {upcomingReservations.length > 0 ? (
                    upcomingReservations.map((reserva, index) => (
                      <tr key={index}>
                        <td className="px-3 py-2 font-medium text-gray-900">{reserva.installation_name}</td>
                        <td className="px-3 py-2">{reserva.data_reserva}</td>
                        <td className="px-3 py-2">
                          {reserva.horario_inicio} - {reserva.horario_fim}
                        </td>
                        <td className="px-3 py-2">{reserva.responsible_name}</td>
                      </tr>
                    ))
                  ) : (
                    <tr>
                      <td className="px-3 py-4 text-gray-500" colSpan={4}>
                        Nenhuma reserva agendada.
                      </td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
          </div>

          <div className="rounded-lg bg-white p-4 shadow">
            <h2 className="text-lg font-semibold text-gray-900">Inscrições em atividades</h2>
            <div className="mt-4 space-y-3">
              {activityEnrollment.length > 0 ? (
                activityEnrollment.map((activity, index) => (
                  <div key={index} className="rounded border border-gray-100 p-3">
                    <div className="flex items-center justify-between">
                      <p className="font-semibold text-gray-900">{activity.nome_atividade}</p>
                      <p className="text-sm text-gray-500">{activity.weekday}</p>
                    </div>
                    <p className="text-sm text-gray-500">
                      {activity.horario_inicio} - {activity.horario_fim}
                    </p>
                    <p className="text-xs text-gray-400">
                      Grupo: {activity.grupo_extensao || '—'}
                    </p>
                    <div className="mt-2 h-2 rounded bg-gray-100 overflow-hidden">
                      <div
                        className="h-2 rounded bg-[#1094ab]"
                        style={{
                          width: `${Math.min(activity.occupancy_rate, 100)}%`,
                        }}
                      ></div>
                    </div>
                    <p className="mt-1 text-xs text-gray-500">
                      {activity.vagas_ocupadas} / {activity.vagas_limite} vagas
                    </p>
                  </div>
                ))
              ) : (
                <p className="text-sm text-gray-500">Nenhuma atividade encontrada.</p>
              )}
            </div>
          </div>
        </div>
      </section>
    </Layout>
    </ProtectedRoute>
  );
}
