import { Link } from 'react-router-dom';
import '../App.css';

function Homepage() {
  return (
    <div className="container">
      <div className="card-body col text-center">
        <h2>Home</h2>
      </div>
      <div className="card-body">
        <div className="row justify-content-md-center">
          <div className="col col-4 text-center">
            <Link to="/">
              <button className="btn btn-primary btn-large w-100">Home</button>
            </Link>
          </div>
        </div>
        <div className="row justify-content-md-center">
          <div className="col col-4 text-center">
            <Link to="/store-key">
              <button className="btn btn-primary btn-large w-100">Store Key</button>
            </Link>
          </div>
        </div>
        <div className="row justify-content-md-center">
          <div className="col col-4 text-center">
            <Link to="/retrieve-key">
              <button className="btn btn-primary btn-large w-100">Retrieve Key</button>
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Homepage;