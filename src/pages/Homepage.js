import { Link } from 'react-router-dom';
import '../App.css';

function Homepage() {
  return (
    <div className="centre-horizontal" style={{ 'textAlign': 'center' }} >
      <h2>Home</h2>
      <Link to="/">
        <button>Home</button>
      </Link>
      <Link to="/store-key">
        <button>Store Key</button>
      </Link>
      <Link to="/retrieve-key">
        <button>Retrieve Key</button>
      </Link>
    </div>
  );
}

export default Homepage;