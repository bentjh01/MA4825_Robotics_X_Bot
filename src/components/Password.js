import '../App.css';
import '../scss/style.scss';

//Component
function Password({ onPasswordChange }) {
  
  function handleChange(event) {
    const val = event.target.value
    onPasswordChange(val);
    console.log("finished pw")
  }

  return (
    <div>
      <div>Password</div>
      <input 
        id="password" 
        className="login"
        maxLength="6"
        onChange={event => handleChange(event)}
      />
    </div>
  );
}


// class Password extends Component {

//   constructor(props) {
//     super(props);
//     this.controllers = {};
//     // this.state = {
//     //   buttons: [0,0,0,0],
//     //   axes: [0,0,0,0],w
//     //   sticks: [0,0]
//     // };
//   }

//   componentDidMount() {
//     /*
//     // If there is an error on the backend, an 'error' emit will be emitted.
//     this.ros.on('error', function (error) {
//       console.log(error);
//     });

//     // Find out exactly when we made a connection.
//     this.ros.on('connection', function () {
//       console.log('Connection made!');
//     });

//     this.ros.on('close', function () {
//       console.log('Connection closed.');
//     });

//     this.ros.connect(this.props.rosbridgeAddress);

//     this.topic = new ROSLIB.Topic({
//       // ros: this.ros,
//       // name: '/joy',
//       // messageType: 'sensor_msgs/Joy'
//     });

//     setInterval(this.timerEnd, 20);
//     */
//   }

//   componentWillUnmount () {
//     // this.ros.close();
//   }


//   render() {
//     return (
//       <div>
//         <div>Password</div>
//         <input 
//           id="password" 
//           type="number"
//           min="1"
//           max="999999" 
//           class="login"
//         />
//       </div>
//     );
//   }
// }

export default Password;
