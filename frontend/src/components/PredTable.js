import React from 'react'
import PredTableRow from './PredTableRow'

const PredTable = ({ predictions }) => {
  return (
    <div className="card h-100">
      <div className="card-body">
        <h5 className="card-title">Predictions From the Past 7 Days</h5>
        <div className="table-responsive">
          <table className="table">
            <thead>
              <tr>
                <th scope="col">#</th>
                <th scope="col">Date</th>
                <th scope="col">Sentiment</th>
                <th scope="col">Prediction</th>
                <th scope="col">Prediction with Sentiment</th>
                <th scope="col">Actual</th>
                <th scope="col">Error</th>
              </tr>
            </thead>

            <tbody>
              {predictions.map((prediction) => (
                <PredTableRow key={prediction.id} prediction={prediction} />
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}

export default PredTable