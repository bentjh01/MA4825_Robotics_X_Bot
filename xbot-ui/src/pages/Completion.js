import { Link } from 'react-router-dom';
import '../App.css';
import '../scss/style.scss';

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
    </div>
  );
}

export default Completion;
