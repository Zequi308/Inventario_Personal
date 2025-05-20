import { useEffect, useState } from 'react';
import axios from 'axios';

function ItemList() {
  const [items, setItems] = useState([]);

  useEffect(() => {
    const fetchItems = async () => {
      try {
        const res = await axios.get('http://localhost:8001/items/', {
          headers: { Authorization: `Bearer ${localStorage.getItem('token')}` },
        });
        setItems(res.data);
      } catch (error) {
        alert('Error al cargar ítems');
      }
    };
    fetchItems();
  }, []);

  const handleDelete = async (id) => {
    try {
      await axios.delete(`http://localhost:8001/items/${id}`, {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` },
      });
      setItems(items.filter((item) => item.id !== id));
    } catch (error) {
      alert('Error al eliminar ítem');
    }
  };

  return (
    <div className="container">
      <h2>Mis Ítems</h2>
      <ul>
        {items.map((item) => (
          <li key={item.id}>
            {item.name} (Cantidad: {item.quantity})
            <button onClick={() => handleDelete(item.id)}>Eliminar</button>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default ItemList;