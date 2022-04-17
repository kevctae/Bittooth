import React from 'react'

const Card = ({ card, onClick }) => {
  return (
    <div className="col-lg-4 my-3">
      <div className="card" width="18rem">
        <div className="card-body">
          <h5 className="card-title">{card.title}</h5>

          <p className="card-text">
            {card.text}
          </p>

          <h1 className="display-2 mb-3 text-center text-secondary">{card.value}</h1>

          <button onClick={() => onClick(card.id)} className="btn btn-primary text-secondary">{card.button_text}</button>
        </div>
      </div>
    </div>
  )
}

export default Card