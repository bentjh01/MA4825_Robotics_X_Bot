import '../App.css';
import '../scss/style.scss';
import React, { useEffect } from 'react';
import ROSLIB from 'roslib';

/**
 * 
 * @param {string} ip private ip address of router/ hotspot
 * @param {string} data the locker number
 * @param {string} action store/retrieve
 * 
 * @return Connection, empty div component
 */
function Connection({ ip, data, action }) {
  const ros = new ROSLIB.Ros();
  
  function intialiseRos() {
    ros.connect(`ws://${ip}:9090`);

    ros.on('connetion', () => {
      console.log("ROS connection established!")
    })

    ros.on('error', (error) => {
      console.log("ROS connection error", error)
    })

    ros.on('close', () => {
      console.log("ROS connection closed.")
    })

    let ui = new ROSLIB.Topic({
      ros: ros,
      name: "/ui",
      messageType: "std_msgs/String"
    })

    let locker = new ROSLIB.Message({
      data: `${data}${action}`,
    })

    console.log("publishing ui", locker);
    ui.publish(locker);
    console.log("published successfuly")
  }

  // mounting starts, and unmounting starts
  useEffect(() => {
    intialiseRos();

    return (() => {
      ros.close();
    })
  })


  return (
    <div>
      ROS Connection
    </div>
  );
}

export default Connection;
