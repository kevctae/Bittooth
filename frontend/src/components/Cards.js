import React from 'react'
import Card from './Card'

const Cards = ({ cards, onClick }) => {
  return (
    <>
      {cards.map((card) => (
        <Card key={card.id} card={card} onClick={onClick} />
      ))}
    </>
  )
}

export default Cards