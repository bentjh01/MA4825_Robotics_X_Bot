// import '../scss/style.scss';
import Login from './Login'

function RetrieveKey() {
  return (
    <div className="my-5 text-center">
      <h2>Retrieve Key</h2>
      <Login action="retrieve"/>
    </div>
  );
}
  
export default RetrieveKey;