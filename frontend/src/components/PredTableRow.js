import React from "react";

const PredTableRow = ({ prediction }) => {
  const formatDate = (date) => {
    if (date !== undefined) {
      const date_obj = new Date(date.$date);
      return date_obj.toLocaleDateString("en-US");
    }
  };
  const formatSentiment = (value) => {
    if (value !== undefined) {
      return value.toFixed(2).toString();
    }
  };

  const formatDollar = (value) => {
    if (value !== undefined) {
      return (
        "$" +
        value
          .toFixed()
          .toString()
          .replace(/\B(?=(\d{3})+(?!\d))/g, ",")
      );
    }
  };

  const formatActVal = (value) => {
    if (value !== undefined) {
      if (value === 0) {
        return "TBA";
      } else {
        return (
          "$" +
          value
            .toFixed()
            .toString()
            .replace(/\B(?=(\d{3})+(?!\d))/g, ",")
        );
      }
    }
  };

  const getError = (pred, actual) => {
    if (pred !== undefined) {
      if (actual === 0) {
        return "TBA";
      } else {
        const error = Math.abs((pred - actual) / actual) * 100;
        return error.toFixed(2).toString() + "%";
      }
    }
  };

  return (
    <tr>
      <th scope="row">{prediction.index + 1}</th>
      <td>{formatDate(prediction.date)}</td>
      <td>{formatSentiment(prediction.sentiment)}</td>
      <td>{formatDollar(prediction.pred)}</td>
      <td>{formatDollar(prediction.pred_sent)}</td>
      <td>{formatActVal(prediction.actual_value)}</td>
      <td>{getError(prediction.pred, prediction.actual_value)} ({getError(prediction.pred_sent, prediction.actual_value)})</td>
    </tr>
  );
};

export default PredTableRow;
