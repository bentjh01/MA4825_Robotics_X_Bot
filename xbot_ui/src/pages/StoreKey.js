// import '../scss/style.scss';
import Login from './Login'

function RetrieveKey() {
  return (
    <div className="my-5 text-center">
      <h2>Store Key</h2>
      <Login action="store"/>
    </div>
  );
}
  
export default RetrieveKey;