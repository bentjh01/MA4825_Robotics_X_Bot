import { Link } from 'react-router-dom';
import '../App.css';

function Homepage() {
  return (
    <div className="container">
      <div className="mb-4 text-center">
        <h1>XBOT</h1>
      </div>
      <div className="card-body my-4 text-center">
        <h2>Home</h2>
      </div>
      <div className="card-body">
        <div className="row my-4 justify-content-md-center">
          <div className="col col-3 text-center">
            <Link to="/">
              <button className="btn btn-primary btn-large w-100"><h4>Home</h4></button>
            </Link>
          </div>
        </div>
        <div className="row my-4 justify-content-md-center">
          <div className="col col-3 text-center">
            <Link to="/store-key">
              <button className="btn btn-primary btn-large w-100"><h4>Store Key</h4></button>
            </Link>
          </div>
        </div>
        <div className="row my-4 justify-content-md-center">
          <div className="col col-3 text-center">
            <Link to="/retrieve-key">
              <button className="btn btn-primary btn-large w-100"><h4>Retrieve Key</h4></button>
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Homepage;