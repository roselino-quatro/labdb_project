'use client';

import { useState, useEffect } from 'react';
import Layout from '@/components/Layout';

interface Participation {
  participant_name: string;
  participant_email: string;
  activity_name: string;
  host_name: string;
  host_nusp: string;
}

export default function ExternalDashboardPage() {
  const [participations, setParticipations] = useState<Participation[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadParticipations();
  }, []);

  const loadParticipations = async () => {
    try {
      const response = await fetch('http://localhost:5050/external/dashboard', {
        credentials: 'include',
      });

      if (response.ok) {
        const html = await response.text();
        // Parse HTML ou fazer chamada API JSON se disponível
        setParticipations([]);
      }
    } catch (err) {
      console.error('Erro ao carregar participações:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Layout>
      <section className="space-y-6">
        <header>
          <h1 className="text-2xl font-semibold text-gray-900">Convites externos</h1>
        </header>

        <div className="overflow-x-auto rounded-lg bg-white shadow">
          <table className="min-w-full text-sm">
            <thead className="border-b text-left text-gray-500">
              <tr>
                <th className="px-4 py-3">Participante</th>
                <th className="px-4 py-3">E-mail</th>
                <th className="px-4 py-3">Atividade</th>
                <th className="px-4 py-3">Anfitrião</th>
                <th className="px-4 py-3">NUSP do Anfitrião</th>
              </tr>
            </thead>
            <tbody className="divide-y">
              {participations.length > 0 ? (
                participations.map((record, index) => (
                  <tr key={index}>
                    <td className="px-4 py-3 font-medium text-gray-900">{record.participant_name}</td>
                    <td className="px-4 py-3">{record.participant_email}</td>
                    <td className="px-4 py-3">{record.activity_name}</td>
                    <td className="px-4 py-3">{record.host_name}</td>
                    <td className="px-4 py-3">{record.host_nusp}</td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td className="px-4 py-6 text-center text-gray-500" colSpan={5}>
                    Não há convites para participantes externos.
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
