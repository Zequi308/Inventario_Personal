import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import Login from './components/Login';
import ItemList from './components/ItemList';
import ItemForm from './components/ItemForm';
import Dashboard from './pages/Dashboard';
import AdminPanel from './pages/AdminPanel';
import Home from './pages/Home';

function App() {
  return (
    <Router>
      <Switch>
        <Route exact path="/" component={Home} />
        <Route path="/login" component={Login} />
        <Route path="/dashboard" component={Dashboard} />
        <Route path="/admin" component={AdminPanel} />
      </Switch>
    </Router>
  );
}

export default App;