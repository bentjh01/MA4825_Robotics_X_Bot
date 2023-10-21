import '../App.css';
import '../scss/style.scss';
import React, { useState, useEffect, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import Locker from './Locker';
import Password from './Password';
import LoginButton from './LoginButton';

function LoginForm({ action }) {
  const navigate = useNavigate();

  // const [lockers, setLockers] = useState([]);
  const [locker, setLocker] = useState('');
  const [pw, setPw] = useState('');
  const [disableButton, setDisableButton] = useState(true);
  const [path, setPath] = useState('');

  // intilialise if new session, or get updated value from chrome.
  let lockers = JSON.parse(sessionStorage.getItem("lockers")); // important to stringify
  console.log(lockers)

  function handleLockerChange(locker) {
    setLocker(locker);
    // console.log("loginForm pw", pw)
  }

  function handlePwChange(pw) {
    setPw(pw);
    // console.log("loginForm pw", pw)
  }

  // set to be callback function
  const checkEmptyInputs = useCallback(() => {
    // console.log("Locker input", locker)
    // console.log("PW input", pw)
    if (locker === '' || pw === '')  {
      setDisableButton(true);
    }
    else {
      setDisableButton(false);
    }
  }, [locker, pw]);

  function checkEmptyLocker() {
    return !lockers.some(item => item === locker);
  }

  function checkPassword() {
    return (locker.repeat(6) === pw && locker !== '');
  }

  function storeSuccess() {
    if (checkPassword()) {
      if (checkEmptyLocker()){
        lockers.push(locker);           // add into array
        lockers.sort((a, b) => a - b);  // and sort
        sessionStorage.setItem("lockers", JSON.stringify(lockers))
        setPath('/completion');
        return true
      }
      else {
        alert(`Locker ${locker} is taken, please choose another locker`);
        return false;
      }
    }
    else {
      alert("Failed, pls try again")
      return false;
    }
  }

  function retrieveSuccess() {
    if (checkPassword()) {
      if (!checkEmptyLocker()){
        lockers = lockers.filter(item => item !== locker) // remove from array
        sessionStorage.setItem("lockers", JSON.stringify(lockers))
        setPath('/completion');
        return true
      }
      else {
        alert(`Nothing inside locker ${locker}, please choose another locker`);
        return false;
      }
    }
    else {
      alert("Failed, pls try again")
      return false;
    }
  }

  function loginSuccess () {
    if (action === "store") {
      return storeSuccess();
    }
    else if (action === "retrieve") {
      return retrieveSuccess();
    }
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
    navigate(path, { state: { 
      action: action,
      data: locker }});
  }, [path, navigate, action, locker])

  return (
    <div className="container">
      <div className="card-body">
        <div className="row py-2 text-center">
          <Locker onLockerChange={handleLockerChange} />
        </div>
        <div className="row py-2 text-center">
          <Password onPasswordChange={handlePwChange} />
        </div>
        <div className="row py-2 text-center">
          <LoginButton 
            onClick={loginSuccess}
            disabled={disableButton}
          />
        </div>
      </div>
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
