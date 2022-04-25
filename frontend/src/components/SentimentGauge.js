import React from "react";
import ReactSpeedometer from "react-d3-speedometer";

const SentimentGauge = ({ value }) => {
  return (
    <div className="card h-100">
      <div className="card-body">
        <h5 className="card-title">Bit-O-Meter</h5>

        <div className="text-center m-3">
          {value === "" ? (
            <div className="d-flex justify-content-center my-5">
              <div className="spinner-border text-primary" role="status">
                <span className="visually-hidden">Loading...</span>
              </div>
            </div>
          ) : (
            <ReactSpeedometer
              className="text-center"
              minValue={-1}
              maxValue={1}
              value={parseFloat(value)}
              maxSegmentLabels={0}
              width={300}
              height={200}
              valueFormat={"d"}
              textColor={"#AAA"}
              currentValueText={"Sentiment Level"}
            />
          )}
        </div>

        <p className="card-text">
          The "Bit-O-Meter" indicates the current Twitter sentiment towards
          "Bitcoin". It should be taken with a grain of salt and should{" "}
          <b>NOT</b> be considered as a factor in your financial investment
          decision. We will not be responsible for any financial liabilities.
        </p>
      </div>
    </div>
  );
};

export default SentimentGauge;
