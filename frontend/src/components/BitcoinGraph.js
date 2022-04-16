import React from 'react'

const BitcoinGraph = () => {
  return (
    <div style={{height: '560px', backgroundColor: '#FFFFFF', overflow: 'hidden', boxSizing: 'border-box', border: '1px solid #56667F', borderRadius: '4px', textAlign: 'right', lineHeight: '14px', fontSize: '12px', fontFeatureSettings: 'normal', textSizeAdjust: '100%', boxShadow: 'inset 0 -20px 0 0 #56667F', padding: '0px', margin: '0px', width: '100%'}}>
      <div style={{height: '540px', padding: '0px', margin: '0px', width: '100%'}}>
        <iframe
          title="coinlib"
          src="https://widget.coinlib.io/widget?type=chart&theme=light&coin_id=859&pref_coin_id=1505"
          width="100%"
          height="536px"
          scrolling="auto"
          marginWidth={0}
          marginHeight={0}
          frameBorder={0}
          border={0}
          style={{border: 0, margin: 0, padding: 0, lineHeight: '14px'}} />
      </div>
      <div style={{color: '#FFFFFF', lineHeight: '14px', fontWeight: 400, fontSize: '11px', boxSizing: 'border-box', padding: '2px 6px', width: '100%', fontFamily: 'Verdana, Tahoma, Arial, sans-serif'}}>
        <a 
          href="https://coinlib.io" 
          target="_blank" 
          rel="noreferrer"
          style={{fontWeight: 500, color: '#FFFFFF', textDecoration: 'none', fontSize: '11px'}}>
          Cryptocurrency Prices
        </a>
        &nbsp;by Coinlib
      </div>
    </div>
  )
}

export default BitcoinGraph