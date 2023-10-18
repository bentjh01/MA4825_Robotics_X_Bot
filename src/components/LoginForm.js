import '../App.css';
import '../scss/style.scss';
import React, { useState, useEffect, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
// import ROSLIB from 'roslib';
import Locker from './Locker';
import Password from './Password';
import LoginButton from './LoginButton';

function LoginForm() {
  const navigate = useNavigate();

  // const [lockers, setLockers] = useState([]);
  const [locker, setLocker] = useState('');
  const [pw, setPw] = useState('');
  const [disableButton, setDisableButton] = useState(true);
  const [path, setPath] = useState('');

  let lockers = JSON.parse(sessionStorage.getItem("lockers"));
  console.log(lockers)

  function handleLockerChange(locker) {
    setLocker(locker);
    console.log("loginForm pw", pw)
  }

  function handlePwChange(pw) {
    setPw(pw);
    console.log("loginForm pw", pw)
  }

  // set to be callback function
  const checkEmptyInputs = useCallback(() => {
    console.log("Locker input", locker)
    console.log("PW input", pw)
    if (locker === '' || pw === '')  {
      setDisableButton(true);
    }
    else {
      setDisableButton(false);
    }
  }, [locker, pw]);

  function checkEmptyLocker() {
    console.log("lockers array", lockers)
    return !lockers.some(item => locker === item);
  }

  function checkPassword() {
    console.log("loginForm Locker", locker)
    console.log("loginForm pw", pw)
    
    if (locker.repeat(6) === pw && locker !== '') {
      setPath('/completion')
      console.log("Unlock Locker!")
      return true
    }
    else {
      alert("Failed, pls try again")
      return false;
    }
  }

  function loginSuccess() {
    if (checkEmptyLocker() && checkPassword()){
      lockers.push(locker);
      lockers.sort((a, b) => a - b);
      console.log(lockers);
      // setLockers(lockers)
      return true
    }
    return false;
  }

  // Update if locker input change
  useEffect(() => {
    checkEmptyInputs();
  }, [locker, checkEmptyInputs])

  // Update if password input change
  useEffect(() => {
    checkEmptyInputs();
  }, [pw, checkEmptyInputs])

  // Update if Submit button is pressed
  useEffect(() => {
    console.log(path)
    navigate(path);
  }, [path, navigate])

  return (
    <div>
        <Locker onLockerChange={handleLockerChange} />
        <Password onPasswordChange={handlePwChange} />
        <LoginButton 
          onClick={loginSuccess}
          disabled={disableButton}
        />
    </div>
  );
}

/*
class LoginForm extends Component {

  constructor(props) {
    super(props);
    this.state = {
      locker: '',
      pw: '',
      disableButton: true,
      path: '',
    };
  
    // this.ros = new ROSLIB.Ros();
  }

  componentDidMount() {
    // If there is an error on the backend, an 'error' emit will be emitted.
    // this.ros.on('error', function (error) {
    //   console.log(error);
    // });

    // // Find out exactly when we made a connection.
    // this.ros.on('connection', function () {
    //   console.log('Connection made!');
    // });

    // this.ros.on('close', function () {
    //   console.log('Connection closed.');
    // });

    // this.ros.connect(this.props.rosbridgeAddress);

    // this.topic = new ROSLIB.Topic({
      // ros: this.ros,
      // name: '/joy',
      // messageType: 'sensor_msgs/Joy'
    // });

    // setInterval(this.timerEnd, 20);
  }

  componentWillUnmount () {
    // this.ros.close();
  }



  timerEnd = () => {

    // var joyMsg = new ROSLIB.Message({
    //   header:
    //   {
    //     // seq: 0,
    //     stamp: [0,0],
    //     frame_id: ""
    //   },
    //   axes: [],
    //   buttons: []
    // });


    // joyMsg.axes = this.state.axes;
    // joyMsg.buttons = this.state.buttons;

    // this.topic.publish(joyMsg);
  }

  handleLockerChange = (locker) => {
    this.setState({locker: locker}, () => {
      this.checkEmptyInputs();
    });
  }

  handlePwChange = (pw) => {
    this.setState({pw: pw}, () => {
      this.checkEmptyInputs()
    });
  }

  checkEmptyInputs = () => {
    console.log("Locker input", this.state.locker)
    console.log("PW input", this.state.pw)
      if (this.state.locker === '' || this.state.pw === '')  {
        this.setState({disableButton: true});
      }
      else {
        this.setState({disableButton: false});
      }
    }

  checkPassword = () => {
    console.log("loginForm Locker", this.state.locker)
    console.log("loginForm pw", this.state.pw)

    if (this.state.locker.repeat(6) === this.state.pw) {
      this.setState({path: '/completion'}, () => {
        this.navigate(this.state.path)
      })
      console.log("Unlock Locker!")
    }
    else {
      console.log("Failed, pls try again")
    }
  }

  render() {
    return (
      <div>
        <Locker onLockerChange={this.handleLockerChange} />
        <Password onPasswordChange={this.handlePwChange} />
        <LoginButton 
          path={this.state.path}
          onClick={this.checkPassword}
          disabled={this.state.disableButton}
        />
        {this.state.path}
    </div>
    );
  }
}
*/

export default LoginForm;
