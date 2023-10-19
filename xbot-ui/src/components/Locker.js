import '../App.css';
import '../scss/style.scss';

// Component
function Locker({ onLockerChange }) {
  
  function handleChange(event) {
    let val = event.target.value;
    val = val.replace(/\D/g|0, '');
    onLockerChange(val);
  }

  return (
    <div>
      <div>Locker</div>
      <input 
        id="locker" 
        className="login"
        maxLength="1"
        onChange={event => handleChange(event)}
      />
    </div>
  );
}

/*
class Locker extends Component {

  constructor(props) {
    super(props);
    this.controllers = {};
    this.state = {
      value: 1,
    }
  }

  handleChange = (event) => {
    let val = event.target.value;
    val = val.replace(/\D/g|0, '');
    this.props.onLockerChange(val);
    console.log(val);
  }

  render() {
    return (
      <div>
        <div>Locker Number</div>
          <input 
          id="locker" 
          className="login"
          maxLength="1"
          onChange={event => this.handleChange(event)}
        />
      </div>
    );
  }
}
*/

export default Locker;
