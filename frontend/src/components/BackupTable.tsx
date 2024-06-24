'use client';
import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { format } from 'date-fns';
import ReloadButton from './ReloadButton';

interface Backup {
  id: number;
  local_id: string;
  localName?: string | null;
  nombre_db: string;
  ip_addr: string;
  puerto: number;
  trabajo: string;
  rnd: string;
  estado: string;
  datos_adicionales: string;
  fecha_inicio_backup: string;
  fecha_fin_backup: string;
  duracion_backup: string;
}

interface Local {
  ParLoc: string;
  ParLocNom: string;
}

const BackupTable: React.FC = () => {
  const [backups, setBackups] = useState<Backup[]>([]);
  const [localId, setLocalId] = useState('');
  const [startDate, setStartDate] = useState(format(new Date(Date.now() - 15 * 24 * 60 * 60 * 1000), 'yyyy-MM-dd'));
  const [endDate, setEndDate] = useState(format(new Date(Date.now() + 1 * 24 * 60 * 60 * 1000), 'yyyy-MM-dd'));
  
  const [currentPage, setCurrentPage] = useState(1);
  const [itemsPerPage] = useState(10);

  // Consantes para el modal de locales
  const [currentPageLocals, setCurrentPageLocals] = useState(1);
  const itemsPerPageLocals = 20;

  const [isModalOpen, setIsModalOpen] = useState(false);
  const [locals, setLocals] = useState([]);

  useEffect(() => {
    fetchBackups();
  }, [localId, startDate, endDate, currentPage]);

  const fetchBackups = async () => {
    try {
      const response = await axios.get(`${process.env.NEXT_PUBLIC_API_URL}/api/backups`, {
        params: {
            local_id: localId,
            start_date: startDate,
            end_date: endDate === '' ? format(new Date(), 'yyyy-MM-dd') : endDate,
        }
      });

      const sortedBackups = response.data.backups.sort((a: Backup, b: Backup) => {
        // sort by fecha_inicio_backup in descending order and local_id in ascending order
        if (a.local_id !== b.local_id) {
          return a.local_id.localeCompare(b.local_id);
        } else {
          return new Date(b.fecha_inicio_backup).getTime() - new Date(a.fecha_inicio_backup).getTime();
        }
      });

      const backupWithLocalNames = await Promise.all(sortedBackups.map(async (backup: Backup) => {
        const localName = await getLocalName(backup.local_id);
        return {
          ...backup,
          local_id: localName,
        };
      }));

      setBackups(backupWithLocalNames);
    } catch (error: any) {
      throw new Error('Error fetching backups:', error);
    }
  };

  const getLocalName = async (localId: string) => {
    try {
      const response = await axios.get(`${process.env.NEXT_PUBLIC_API_URL}/parlocs/${localId}`);
      return response.data.parloc.ParLocNom;
    } catch (error: any) {
      throw new Error('Error fetching local name:', error);
    }
  }

  const getLocals = async () => {
    try {
      const response = await axios.get(`${process.env.NEXT_PUBLIC_API_URL}/parlocs`);
      setLocals(response.data.parlocs);
      setIsModalOpen(true);
    } catch (error: any) {
      throw new Error('Error fetching locals:', error);
    }
  }

  const handleLocalClick = (local: Local) => {
    setLocalId(local.ParLoc);
    setIsModalOpen(false);
  };

  const handlePageChangeLocals = (pageNumber: number) => {
    setCurrentPageLocals(pageNumber);
  };

  // Paginación de locales
  const indexOfLastItemLocals = currentPageLocals * itemsPerPageLocals;
  const indexOfFirstItemLocals = indexOfLastItemLocals - itemsPerPageLocals;
  const currentLocals = locals.slice(indexOfFirstItemLocals, indexOfLastItemLocals);
  const totalPagesLocals = Math.ceil(locals.length / itemsPerPageLocals);

  const paginatedBackups = backups.slice((currentPage - 1) * itemsPerPage, currentPage * itemsPerPage);

  const totalPages = Math.ceil(backups.length / itemsPerPage);

  return (
    <div className="container mx-auto px-4 py-8 bg-gray-900 text-gray-100">
      <div className="flex justify-between items-center my-4">
        <label className="block text-gray-400">
          Local ID:
          <input
            type="text"
            value={localId}
            onChange={(e) => setLocalId(e.target.value)}
            className="bg-gray-800 text-gray-200 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <button
            onClick={getLocals}
            className="px-4 py-2 bg-gray-700 text-gray-300 rounded hover:bg-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500 ml-2"
          >
            🔍
          </button>
        </label>
        {isModalOpen && (
        <div className="fixed inset-0 flex items-center justify-center bg-gray-900 bg-opacity-75">
          <div className="bg-gray-900 p-6 rounded-lg shadow-lg max-w-3xl w-full border border-gray-600">
            <h2 className="text-lg font-bold mb-4">Select a Local</h2>
            <div className="grid grid-cols-2 gap-4">
              {currentLocals.map((local: Local) => (
                <div
                  key={local.ParLoc}
                  className="p-2 border-b hover:bg-gray-800 cursor-pointer transition-colors duration-300"
                  onClick={() => handleLocalClick(local)}
                  onDoubleClick={() => handleLocalClick(local)}
                >
                  {local.ParLocNom} ({local.ParLoc})
                </div>
              ))}
            </div>
            <div className="mt-4 flex justify-between items-center">
              <button
                onClick={() => setIsModalOpen(false)}
                className="px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600"
              >
                Close
              </button>
              <div className="flex space-x-2">
                {[...Array(totalPagesLocals)].map((_, index) => (
                  <button
                    key={index}
                    onClick={() => handlePageChangeLocals(index + 1)}
                    className={`px-3 py-1 rounded ${
                      currentPageLocals === index + 1 ? 'bg-blue-500 text-white' : 'bg-gray-600'
                    }`}
                  >
                    {index + 1}
                  </button>
                ))}
              </div>
            </div>
          </div>
        </div>
      )}
        <label className="block text-gray-400">
          Start Date:
          <input
            type="date"
            value={startDate}
            onChange={(e) => setStartDate(e.target.value)}
            className="bg-gray-800 text-gray-200 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </label>
        <label className="block text-gray-400">
          End Date:
          <input
            type="date"
            value={endDate}
            onChange={(e) => setEndDate(e.target.value)}
            className="bg-gray-800 text-gray-200 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </label>
      </div>
      <table className="min-w-full divide-y divide-gray-700">
        <thead className="bg-gray-800">
          <tr className="text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
            <th className="px-6 py-3">ID</th>
            <th className="px-6 py-3">Local ID</th>
            <th className="px-6 py-3">Nombre DB</th>
            <th className="px-6 py-3">IP Address</th>
            <th className="px-6 py-3">Trabajo</th>
            <th className="px-6 py-3">Estado</th>
            <th className="px-6 py-3">Fecha Inicio</th>
            <th className="px-6 py-3">Fecha Fin</th>
            <th className="px-6 py-3">Duración</th>
          </tr>
        </thead>
        <tbody className="bg-gray-800 divide-y divide-gray-700">
          {paginatedBackups.map((backup: Backup) => (
            <tr key={backup.id} className={backup.estado === 'En proceso' ? 'bg-yellow-600' : 'bg-emerald-700'}>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-300">{backup.local_id}</td>
              {/* nombre local */}
              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-300">{backup.localName}</td>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-300">{backup.ip_addr}</td>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-300">{backup.trabajo}</td>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-300">{backup.estado}</td>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-300">{backup.fecha_inicio_backup}</td>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-300">{backup.duracion_backup} mins.</td>
            </tr>
          ))}
        </tbody>
      </table>
      <div className="flex justify-between items-center mt-4">
        <button
          onClick={() => setCurrentPage((prev) => Math.max(prev - 1, 1))}
          disabled={currentPage === 1}
          className="px-4 py-2 bg-gray-700 text-gray-300 rounded hover:bg-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50"
        >
          Previous
        </button>
        <div className="text-gray-400">
          Page {currentPage} of {totalPages}
        </div>
        <button
          onClick={() => setCurrentPage((prev) => (!backups.length || currentPage === totalPages ? prev : prev + 1))}
          disabled={currentPage === totalPages}
          className="px-4 py-2 bg-gray-700 text-gray-300 rounded hover:bg-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50"
        >
          Next
        </button>
      </div>
      <ReloadButton onClick={fetchBackups} />
    </div>
  );
};

export default BackupTable;
