import React from 'react'

const Card = ({ card }) => {
  return (
    <div className="col-lg-4 mt-3">
      <div className="card h-100" width="18rem">
        <div className="card-body">
          {card.value === "" ? (
            <div className="d-flex justify-content-center my-5">
              <div className="spinner-border text-primary" role="status">
                <span className="visually-hidden">Loading...</span>
              </div>
            </div>
          ) : (
            <h1 className="display-2 my-5 text-center text-secondary">{card.value}</h1>
          )}

          <h5 className="card-title">{card.title}</h5>

          <p className="card-text">
            {card.text}
          </p>
        </div>
      </div>
    </div>
  )
}

export default Card