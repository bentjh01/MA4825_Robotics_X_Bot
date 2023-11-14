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
    text = "Please put your key on XBOT, \nXBOT will store it";
  }
  else if (action === "retrieve") {
    text = "XBOT is getting your key, \nplease collect it.";
  }

  return (
    <div className="container d-flex center">
      <div className="card-body">
        <div className="row py-2 text-center multiline">
          <h3>
            <p>Log in success</p>
            <p>{text}</p>
          </h3>
        </div>
        <div className="row py-2 text-center">
          <HomeButton />
        </div>
        <div className="row py-2 d-flex text-center">
          <Connection ip="10.42.0.1" data={data} action={action} />
        </div>
      </div>
    </div>
  );
}

export default Completion;
