import { Link } from 'react-router-dom';
import '../App.css';

function Homepage() {
  return (
    <div className="container">
      <div className="mb-5 text-center">
        <h1>XBOT</h1>
      </div>
      <div className="card-body my-5 text-center">
        <h2>Home</h2>
      </div>
      <div className="card-body">
        <div className="row py-5 justify-content-center">
          <div className="col col-8 col-sm-4 col-md-3 text-center">
            <Link to="/store-key">
              <button className="btn btn-primary btn-large w-100 py-3"><h4>Store Key</h4></button>
            </Link>
          </div>
        </div>
        <div className="row py-5 justify-content-center">
          <div className="col col-8 col-sm-4 col-md-3 text-center">
            <Link to="/retrieve-key">
              <button className="btn btn-primary btn-large w-100 py-3"><h4>Retrieve Key</h4></button>
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Homepage;