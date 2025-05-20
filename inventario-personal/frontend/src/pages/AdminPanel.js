import { useEffect, useState } from 'react';
import axios from 'axios';

function AdminPanel() {
  const [roles, setRoles] = useState([]);

  useEffect(() => {
    const fetchRoles = async () => {
      try {
        const res = await axios.get('http://localhost:8002/roles/', {
          headers: { Authorization: `Bearer ${localStorage.getItem('token')}` },
        });
        setRoles(res.data);
      } catch (error) {
        alert('Error al cargar roles');
      }
    };
    fetchRoles();
  }, []);

  return (
    <div className="container">
      <h1>Panel de Administración</h1>
      <h2>Roles</h2>
      <ul>
        {roles.map((role) => (
          <li key={role.id}>{role.name}</li>
        ))}
      </ul>
    </div>
  );
}

export default AdminPanel;