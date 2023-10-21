import { useLocation } from 'react-router-dom';
import '../App.css';
import '../scss/style.scss';
import Connection from '../components/Connection'
import HomeButton from '../components/HomeButton'

/**
 * Mounting connection, and unmount when leaving this page
 */
function Completion() {
  const location = useLocation();
  let text;
  console.log(location.state.action)
  console.log(location.state.data)
  if (location.state.action === "store") {
    text = "Log in success!\nXBOT is putting your key.";
  }
  else if (location.state.action === "retrieve") {
    text = "Log in success!\nXBOT is getting your key.";
  }

  return (
    <div className="container">
      <div className="card-body">
        <div className="row py-2 text-center">
          <h3>{text}</h3>
        </div>
        <div className="row my-4 py-2 text-center">
          <HomeButton />
        </div>
        <div className="row py-2 text-center">
          <Connection ip="192.168.0.1" data={location.state.data}/>
        </div>
      </div>
    </div>
  );
}

export default Completion;
