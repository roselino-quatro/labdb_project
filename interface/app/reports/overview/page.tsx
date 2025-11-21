'use client';

import { useState, useEffect } from 'react';
import Layout from '@/components/Layout';
import { apiGet } from '@/lib/api';

interface ReservationRollup {
  installation_name: string | null;
  month_number: number | null;
  total_reservations: number;
}

interface ActivitiesCube {
  council_number: string | null;
  category: string | null;
  total_activities: number;
}

interface ParticipantsTotal {
  activity_name: string | null;
  total_participants: number;
}

interface InstallationRanking {
  ranking: number;
  installation_name: string;
  total_reservations: number;
}

export default function ReportsOverviewPage() {
  const [reservationRollup, setReservationRollup] = useState<ReservationRollup[]>([]);
  const [activitiesCube, setActivitiesCube] = useState<ActivitiesCube[]>([]);
  const [participantsTotals, setParticipantsTotals] = useState<ParticipantsTotal[]>([]);
  const [installationRanking, setInstallationRanking] = useState<InstallationRanking[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadReports();
  }, []);

  const loadReports = async () => {
    try {
      const data = await apiGet<{
        success: boolean;
        reservation_rollup: ReservationRollup[];
        activities_cube: ActivitiesCube[];
        participants_totals: ParticipantsTotal[];
        installation_ranking: InstallationRanking[];
      }>('/reports/');

      if (data.success) {
        setReservationRollup(data.reservation_rollup || []);
        setActivitiesCube(data.activities_cube || []);
        setParticipantsTotals(data.participants_totals || []);
        setInstallationRanking(data.installation_ranking || []);
      }
    } catch (err) {
      console.error('Erro ao carregar relatórios:', err);
      setReservationRollup([]);
      setActivitiesCube([]);
      setParticipantsTotals([]);
      setInstallationRanking([]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Layout>
      <section className="space-y-6">
        <header>
          <h1 className="text-2xl font-semibold text-gray-900">Relatórios operacionais</h1>
        </header>

        <div className="grid gap-6 lg:grid-cols-2">
          <div className="rounded-lg bg-white p-4 shadow">
            <h2 className="text-lg font-semibold text-gray-900">Consolidado de reservas</h2>
            <div className="mt-4 max-h-96 overflow-x-auto overflow-y-auto">
              <table className="min-w-full text-sm">
                <thead className="border-b text-left text-gray-500">
                  <tr>
                    <th className="px-3 py-2">Instalação</th>
                    <th className="px-3 py-2">Mês</th>
                    <th className="px-3 py-2">Total</th>
                  </tr>
                </thead>
                <tbody className="divide-y">
                  {reservationRollup.length > 0 ? (
                    reservationRollup.map((row, index) => (
                      <tr key={index}>
                        <td className="px-3 py-2">{row.installation_name || 'Total'}</td>
                        <td className="px-3 py-2">{row.month_number || '—'}</td>
                        <td className="px-3 py-2 font-semibold text-gray-900">{row.total_reservations}</td>
                      </tr>
                    ))
                  ) : (
                    <tr>
                      <td className="px-3 py-6 text-center text-gray-500" colSpan={3}>
                        Nenhum dado de reserva disponível.
                      </td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
          </div>

          <div className="rounded-lg bg-white p-4 shadow">
            <h2 className="text-lg font-semibold text-gray-900">Atividades por educador</h2>
            <div className="mt-4 max-h-96 overflow-x-auto overflow-y-auto">
              <table className="min-w-full text-sm">
                <thead className="border-b text-left text-gray-500">
                  <tr>
                    <th className="px-3 py-2">Conselho</th>
                    <th className="px-3 py-2">Categoria</th>
                    <th className="px-3 py-2">Total</th>
                  </tr>
                </thead>
                <tbody className="divide-y">
                  {activitiesCube.length > 0 ? (
                    activitiesCube.map((row, index) => (
                      <tr key={index}>
                        <td className="px-3 py-2">{row.council_number || 'Todos'}</td>
                        <td className="px-3 py-2">{row.category || 'Todos'}</td>
                        <td className="px-3 py-2 font-semibold text-gray-900">{row.total_activities}</td>
                      </tr>
                    ))
                  ) : (
                    <tr>
                      <td className="px-3 py-6 text-center text-gray-500" colSpan={3}>
                        Nenhum dado de atividade disponível.
                      </td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
          </div>
        </div>

        <div className="grid gap-6 lg:grid-cols-2">
          <div className="rounded-lg bg-white p-4 shadow">
            <h2 className="text-lg font-semibold text-gray-900">Participantes por atividade</h2>
            <div className="mt-4 max-h-96 overflow-x-auto overflow-y-auto">
              <table className="min-w-full text-sm">
                <thead className="border-b text-left text-gray-500">
                  <tr>
                    <th className="px-3 py-2">Atividade</th>
                    <th className="px-3 py-2">Participantes</th>
                  </tr>
                </thead>
                <tbody className="divide-y">
                  {participantsTotals.length > 0 ? (
                    participantsTotals.map((row, index) => (
                      <tr key={index}>
                        <td className="px-3 py-2">{row.activity_name || 'Total'}</td>
                        <td className="px-3 py-2 font-semibold text-gray-900">{row.total_participants}</td>
                      </tr>
                    ))
                  ) : (
                    <tr>
                      <td className="px-3 py-6 text-center text-gray-500" colSpan={2}>
                        Nenhum dado de participante disponível.
                      </td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
          </div>

          <div className="rounded-lg bg-white p-4 shadow">
            <h2 className="text-lg font-semibold text-gray-900">Ranking de instalações</h2>
            <div className="mt-4 max-h-96 overflow-x-auto overflow-y-auto">
              <table className="min-w-full text-sm">
                <thead className="border-b text-left text-gray-500">
                  <tr>
                    <th className="px-3 py-2">Posição</th>
                    <th className="px-3 py-2">Instalação</th>
                    <th className="px-3 py-2">Reservas</th>
                  </tr>
                </thead>
                <tbody className="divide-y">
                  {installationRanking.length > 0 ? (
                    installationRanking.map((row, index) => (
                      <tr key={index}>
                        <td className="px-3 py-2 font-semibold text-gray-900">#{row.ranking}</td>
                        <td className="px-3 py-2">{row.installation_name}</td>
                        <td className="px-3 py-2">{row.total_reservations}</td>
                      </tr>
                    ))
                  ) : (
                    <tr>
                      <td className="px-3 py-6 text-center text-gray-500" colSpan={3}>
                        Nenhum ranking disponível.
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
