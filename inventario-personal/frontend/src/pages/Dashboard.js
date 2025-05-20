import ItemForm from '../components/ItemForm';
import ItemList from '../components/ItemList';

function Dashboard() {
  return (
    <div className="container">
      <h1>Panel de Control</h1>
      <ItemForm />
      <ItemList />
    </div>
  );
}

export default Dashboard;