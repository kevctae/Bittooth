import React from 'react'
import Card from './Card'

const Cards = ({ cards }) => {
  return (
    <>
      {cards.map((card) => (
        <Card key={card.id} card={card} />
      ))}
    </>
  )
}

export default Cards