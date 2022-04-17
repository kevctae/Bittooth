import React from 'react';
import { useState, useEffect } from 'react';

const Timer = () => {
  const calculateTimeLeft = () => {
    const today = new Date()
    const tomorrow = new Date(today)
    tomorrow.setDate(tomorrow.getDate() + 1)
    tomorrow.setHours(-4, 0, 0, 0)
    const difference = +tomorrow - +today;
    let timeLeft = {};

    if (difference > 0) {
      timeLeft = {
        hr: Math.floor((difference / (1000 * 60 * 60)) % 24),
        min: Math.floor((difference / 1000 / 60) % 60),
        sec: Math.floor((difference / 1000) % 60),
      };
    }

    return timeLeft;
  };

  const [timeLeft, setTimeLeft] = useState(calculateTimeLeft());

  useEffect(() => {
    const timer = setTimeout(() => {
      setTimeLeft(calculateTimeLeft());
    }, 1000);
  
    return () => clearTimeout(timer);
  });

  const timerComponents = [];

  Object.keys(timeLeft).forEach((interval) => {
    if (!timeLeft[interval]) {
      return;
    }

    timerComponents.push(
      <>
        {timeLeft[interval]} {interval}&nbsp;
      </>
    );
  });

  return (
    <div className="card" width="18rem">
      <div className="card-body">
        <div className="d-flex flex-column justify-content-center m-3">
          <h4 className="text-center"><b>Next Prediction:</b></h4>

          <h1 className="display-6 mb-3 text-center text-primary">
            {timerComponents.length ? timerComponents : <span>Refresh Page to Update Value</span>}
          </h1>
        </div>
      </div>
    </div>
  )
}

export default Timer