import { useState } from 'react';
import axios from 'axios';

function ItemForm() {
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  const [quantity, setQuantity] = useState(0);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post(
        'http://localhost:8001/items/',
        { name, description, quantity },
        { headers: { Authorization: `Bearer ${localStorage.getItem('token')}` } }
      );
      alert('Ítem creado');
      setName('');
      setDescription('');
      setQuantity(0);
    } catch (error) {
      alert('Error al crear el ítem');
    }
  };

  return (
    <div className="container">
      <h2>Crear Ítem</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Nombre"
          value={name}
          onChange={(e) => setName(e.target.value)}
        />
        <textarea
          placeholder="Descripción"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
        />
        <input
          type="number"
          placeholder="Cantidad"
          value={quantity}
          onChange={(e) => setQuantity(e.target.value)}
        />
        <button type="submit">Crear</button>
      </form>
    </div>
  );
}

export default ItemForm;