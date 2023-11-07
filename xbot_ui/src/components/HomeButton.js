import { Link } from 'react-router-dom';
import '../App.css';
import '../scss/style.scss';

function HomeButton() {
  return (
    <Link to="/">
      <button className="btn btn-primary btn-large">
        <h4>Home</h4>
      </button>
    </Link>
  );
}

export default HomeButton;
