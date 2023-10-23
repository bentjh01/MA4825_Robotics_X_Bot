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
  let action = location.state.action;
  let data = location.state.data;
  console.log(action)
  console.log(data)
  if (action === "store") {
    text = "Log in success!\nXBOT is putting your key.";
  }
  else if (action === "retrieve") {
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
          <Connection ip="10.42.0.1" data={data} action={action} />
        </div>
      </div>
    </div>
  );
}

export default Completion;