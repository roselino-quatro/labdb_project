'use client';

import { useState, useEffect } from 'react';

export default function DebugButtons() {
  const [loading, setLoading] = useState(false);
  const [loadingMessage, setLoadingMessage] = useState('Processando...');
  const [toast, setToast] = useState<{ message: string; type: 'success' | 'error' } | null>(null);
  const [isPopulated, setIsPopulated] = useState<boolean | null>(null);

  const showLoading = (message: string) => {
    setLoadingMessage(message);
    setLoading(true);
  };

  const hideLoading = () => {
    setLoading(false);
  };

  const showToast = (message: string, type: 'success' | 'error') => {
    setToast({ message, type });
    setTimeout(() => {
      setToast(null);
    }, 5000);
  };

  const checkDatabaseStatus = async () => {
    try {
      const response = await fetch('http://localhost:5050/debug/check-db-status', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include',
      });

      const data = await response.json();
      setIsPopulated(data.populated ?? false);
    } catch (error) {
      console.error('Erro ao verificar estado do banco:', error);
      setIsPopulated(false);
    }
  };

  useEffect(() => {
    checkDatabaseStatus();
  }, []);

  const populateDatabase = async () => {
    if (!confirm('Tem certeza que deseja popular o banco de dados? Isso pode levar alguns minutos.')) {
      return;
    }

    showLoading('Gerando dados sintéticos e populando banco...');

    try {
      const response = await fetch('http://localhost:5050/debug/populate-db', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include',
      });

      const data = await response.json();

      if (data.success) {
        showToast(data.message, 'success');
        setIsPopulated(true);
        setTimeout(() => {
          window.location.reload();
        }, 2000);
      } else {
        showToast(data.message || 'Erro ao popular banco de dados', 'error');
      }
    } catch (error) {
      showToast('Erro ao popular banco de dados: ' + (error instanceof Error ? error.message : 'Erro desconhecido'), 'error');
    } finally {
      hideLoading();
    }
  };

  const clearDatabase = async () => {
    if (!confirm('ATENÇÃO: Tem certeza que deseja APAGAR TODOS os dados do banco? Esta ação não pode ser desfeita!')) {
      return;
    }

    if (!confirm('Confirma novamente: Todos os dados serão PERMANENTEMENTE apagados!')) {
      return;
    }

    showLoading('Limpando banco de dados...');

    try {
      const response = await fetch('http://localhost:5050/debug/clear-db', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include',
      });

      const data = await response.json();

      if (data.success) {
        showToast(data.message, 'success');
        setIsPopulated(false);
        setTimeout(() => {
          window.location.reload();
        }, 2000);
      } else {
        showToast(data.message || 'Erro ao limpar banco de dados', 'error');
      }
    } catch (error) {
      showToast('Erro ao limpar banco de dados: ' + (error instanceof Error ? error.message : 'Erro desconhecido'), 'error');
    } finally {
      hideLoading();
    }
  };

  return (
    <>
      {/* Debug Buttons (Floating) */}
      <div className="fixed bottom-6 right-6 z-[9999] flex flex-col gap-3" style={{ zIndex: 9999 }}>
        <button
          onClick={populateDatabase}
          disabled={loading || isPopulated === true}
          className={`bg-green-600 hover:bg-green-700 text-white font-semibold py-3 px-6 rounded-full shadow-lg transition-all duration-200 transform hover:scale-105 active:scale-95 flex items-center gap-2 disabled:opacity-50 ${!(loading || isPopulated === true) ? 'cursor-pointer' : 'cursor-not-allowed'}`}
          title={isPopulated === true ? "Banco de dados já está populado" : "Popular banco de dados"}
        >
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 4v16m8-8H4"></path>
          </svg>
          <span>Popular DB</span>
        </button>
        <button
          onClick={clearDatabase}
          disabled={loading || isPopulated === false}
          className={`bg-red-600 hover:bg-red-700 text-white font-semibold py-3 px-6 rounded-full shadow-lg transition-all duration-200 transform hover:scale-105 active:scale-95 flex items-center gap-2 disabled:opacity-50 ${!(loading || isPopulated === false) ? 'cursor-pointer' : 'cursor-not-allowed'}`}
          title={isPopulated === false ? "Banco de dados já está vazio" : "Limpar banco de dados"}
        >
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
          </svg>
          <span>Limpar DB</span>
        </button>
      </div>

      {/* Loading Overlay */}
      {loading && (
        <div className="fixed inset-0 bg-black bg-opacity-50 z-[10000] flex items-center justify-center" style={{ zIndex: 10000 }}>
          <div className="bg-white rounded-lg p-6 max-w-sm w-full mx-4">
            <div className="flex items-center gap-4">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
              <div>
                <p className="font-semibold text-gray-900">{loadingMessage}</p>
                <p className="text-sm text-gray-500">Por favor, aguarde</p>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Toast Notification */}
      {toast && (
        <div className="fixed top-6 right-6 z-[9999] max-w-sm w-full" style={{ zIndex: 9999 }}>
          <div
            className={`bg-white rounded-lg shadow-xl p-4 border-l-4 ${
              toast.type === 'success' ? 'border-green-500' : 'border-red-500'
            }`}
          >
            <div className="flex items-start">
              <div className="flex-shrink-0">
                {toast.type === 'success' ? (
                  <svg className="h-6 w-6 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                  </svg>
                ) : (
                  <svg className="h-6 w-6 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                  </svg>
                )}
              </div>
              <div className="ml-3 flex-1">
                <p className="text-sm font-medium text-gray-900">{toast.message}</p>
              </div>
              <button
                onClick={() => setToast(null)}
                className="ml-4 flex-shrink-0 text-gray-400 hover:text-gray-500"
              >
                <svg className="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clipRule="evenodd"></path>
                </svg>
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
}
