import '../App.css';
import '../scss/style.scss';
import LoginForm from '../components/LoginForm'

function Login( { action } ) {
  // let button;

  // if (loginSuccess()) {
  //   button = 
  //     // <Link to="/retrieve-key">
  //       <button>Submit</button>
  //     {/* </Link> */}
  // } else {
  //   button = <button>Submit</button>
  //   // button = <LoginButton onClick={this.handleLoginClick} />;
  // }

  return (
    <LoginForm action={action} />
  );
}



export default Login;
