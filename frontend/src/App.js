import './App.css';
import BitcoinGraph from './components/BitcoinGraph';
import { useState } from 'react';
import Cards from './components/Cards';

const App = () => {
  const [cards, setCards] = useState([
    {
      id: 1,
      title: "Today's Twitter Sentiment Value",
      text: "The following tool calculates the \"Bitcoin\" sentiment value for today. It scrapes verified Twitter Tweets that contains the key value of \"Bitcoin\". The scraped Tweets is cleaned and analyzed using NLP to determine the sentiment value.",
      value: "",
      button_text: "Get Sentiment"
    },
    {
      id: 2,
      title: "Bitcoin Value Prediction",
      text: "The following tool predicts the value of \"Bitcoin\". It predicts by using a Ridge Regression model, which is trained from Jan 2020 to Dec 2021 data.",
      value: "",
      button_text: "Predict"
    },
    {
      id: 3,
      title: "Bitcoin Value Prediction with Sentiment",
      text: "The following tool predicts the value of \"Bitcoin\" with added feature of sentiment from Twitter Tweets. This may may or may not result in improvement of the prediction.",
      value: "",
      button_text: "Predict"
    }
  ])

  const onClick = (id) => {
    switch(id) {
      case 1:
        fetch("http://127.0.0.1:5000/get_sentiment")
          .then(res => res.json())
          .then(result => {
            updateValue(id, result.sentiment);
          })
          .catch(error => {
            console.log(error);
          });
        break;
      case 2:
        fetch("http://127.0.0.1:5000/predict_without_sentiment")
          .then(res => res.json())
          .then(result => {
            updateValue(id, result.predicted_value_without_sentiment);
          })
          .catch(error => {
            console.log(error);
          });
        break;
      default:
        fetch("http://127.0.0.1:5000/predict_with_sentiment")
          .then(res => res.json())
          .then(result => {
            updateValue(id, result.predicted_value_with_sentiment);
          })
          .catch(error => {
            console.log(error);
          });
    }
  }

  const updateValue = (id, value) => {
    const newCards = cards.map((card) => {
      if (card.id === id) {
        let newVal = 0;

        switch(id) {
          case 1:
            newVal = value.toFixed(2).toString()
            break;
          default:
            newVal = "$" + value.toFixed().toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
        }

        const updatedCard = {
          ...card,
          value: newVal,
        };

        return updatedCard;
      }

      return card;
    });

    setCards(newCards)
  }
  
  return (
    <div className="container">
      <div className="row">
        <div className="col mt-3">
          <BitcoinGraph />
        </div>
      </div>

      <div className="row">
        <Cards cards={cards} onClick={onClick} />
      </div>
    </div>
  );
}

export default App;
