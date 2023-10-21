import { Link } from 'react-router-dom';
import '../App.css';
import '../scss/style.scss';
import Connection from '../components/Connection'

/**
 * Mounting connection, and unmount when leaving this page
 */
function Completion() {
  return (
    <div>
      You successfully logged in! 
      The bot will put your key in soon.
      <Link to="/">
        <button>
          OK
        </button>
      </Link>
      <Connection ip="192.168.0.1" data="0"/>
    </div>
  );
}

export default Completion;
