import './App.css';
import { useState, useEffect } from 'react';
import BitcoinGraph from './components/BitcoinGraph';
import Cards from './components/Cards';
import Timer from './components/Timer';
import SentimentGauge from './components/SentimentGauge';

const value_map = {
  0: "sentiment",
  1: "pred",
  2: "pred_sent"
}

const App = () => {
  const [cards, setCards] = useState([
    {
      id: 0,
      title: "Today's Twitter Sentiment Value",
      text: "The following tool calculates the \"Bitcoin\" sentiment value for today. It scrapes verified Twitter Tweets that contains the key value of \"Bitcoin\". The scraped Tweets is cleaned and analyzed using NLP to determine the sentiment value. Value ranges from -1 to 1.",
      value: "",
      button_text: "Get Sentiment"
    },
    {
      id: 1,
      title: "Bitcoin Value Prediction",
      text: "The following tool predicts the value of \"Bitcoin\". It predicts by using a Ridge Regression model, which is trained from Jan 2020 to Dec 2021 data.",
      value: "",
      button_text: "Predict"
    },
    {
      id: 2,
      title: "Bitcoin Value Prediction with Sentiment",
      text: "The following tool predicts the value of \"Bitcoin\" with added feature of sentiment from Twitter Tweets. This may may or may not result in improvement of the prediction.",
      value: "",
      button_text: "Predict"
    }
  ])

  useEffect(() => {
    const updateValue = (values) => {
      const newCards = cards.map((card) => {
        let newVal = values[0][value_map[card.id]];
  
        switch(card.id) {
          case 0:
            newVal = newVal.toFixed(2).toString();
            break;
          default:
            newVal = "$" + newVal.toFixed().toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
        }
  
        const updatedCard = {
          ...card,
          value: newVal,
        };
  
        return updatedCard;
      });
  
      setCards(newCards)
    }

    async function fetchData() {
      try {
        const data = await fetch("http://127.0.0.1:5000/get_predictions")
          .then(res => res.json())

        updateValue(data);
      }
      catch(err) {
        console.log(err);
      };
    }

    fetchData();
  }, [])
  
  return (
    <div className="container">
      <div className="row">
        <div className="col-xl-8 mt-3">
          <BitcoinGraph />
        </div>

        <div className="col-xl-4 mt-3">
          <SentimentGauge value={cards[0].value} />
        </div>
      </div>

      <div className="row">
        <div className="col mt-3">
          <Timer />
        </div>
      </div>

      <div className="row">
        <Cards cards={cards} />
      </div>
    </div>
  );
}

export default App;
