// import React, { Component } from 'react'
import '../App.css';
import '../scss/style.scss';

function LoginButton({ onClick, disabled }) {

  return (
    <div>
      <button 
        id="login-button"
        className="login"
        onClick={onClick}
        disabled={disabled}
      >
        Submit
      </button>
    </div>
  );
}

/*
class LoginButton extends Component {

  constructor(props) {
    super(props);
    this.controllers = {};
    this.state = {
      path: '/',
    };
  }

  render() {
    return (
      <div>
        <button 
          id="login-button"
          className="login"
          onClick={this.props.onClick}
          disabled={this.props.disabled}
        >
          Submit
        </button>
      </div>
    );
  }
}
*/

export default LoginButton;
