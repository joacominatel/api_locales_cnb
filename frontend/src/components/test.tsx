'use client';
import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { format } from 'date-fns';

interface Backup {
  id: number;
  local_id: string;
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

const Backup: React.FC = () => {
  const [backups, setBackups] = useState<Backup[]>([]);
  const [localId, setLocalId] = useState('');
  const [startDate, setStartDate] = useState(format(new Date(Date.now() - 15 * 24 * 60 * 60 * 1000), 'yyyy-MM-dd'));
  const [endDate, setEndDate] = useState(format(new Date(Date.now() + 1 * 24 * 60 * 60 * 1000), 'yyyy-MM-dd'));
  const [currentPage, setCurrentPage] = useState(1);
  const [itemsPerPage] = useState(10);

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
      console.log('response:', response);
      setBackups(response.data.backups);
    } catch (error) {
      console.error('Error fetching backups:', error);
    }
  };

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
    </label>
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
        <th className="px-6 py-3">Puerto</th>
        <th className="px-6 py-3">Estado</th>
        <th className="px-6 py-3">Fecha Inicio</th>
        <th className="px-6 py-3">Fecha Fin</th>
        <th className="px-6 py-3">Duración</th>
      </tr>
    </thead>
    <tbody className="bg-gray-800 divide-y divide-gray-700">
      {paginatedBackups.map((backup) => (
        <tr key={backup.id} className={backup.estado === 'En proceso' ? 'bg-yellow-600' : 'bg-emerald-500'}>
          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-300">{backup.id}</td>
          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-300">{backup.local_id}</td>
          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-300">{backup.nombre_db}</td>
          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-300">{backup.ip_addr}</td>
          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-300">{backup.puerto}</td>
          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-300">{backup.estado}</td>
          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-300">{backup.fecha_inicio_backup}</td>
          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-300">{backup.fecha_fin_backup}</td>
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
</div>
);
};

export default Backup;
