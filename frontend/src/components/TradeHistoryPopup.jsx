import React from 'react';
import { X } from 'lucide-react';

const TradeHistoryPopup = ({ isOpen, onClose, trades, events }) => {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 z-50 flex justify-center items-center">
      <div className="bg-white rounded-lg p-8 max-w-4xl w-full mx-4 max-h-[90vh] overflow-y-auto relative">
        <button
          onClick={onClose}
          className="absolute top-2 right-2 text-gray-500 hover:text-gray-700"
        >
          <X size={24} />
        </button>
        <h2 className="text-2xl font-bold mb-4">Trade History and Events</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <h3 className="text-xl font-semibold mb-2">Trades</h3>
            {Object.entries(trades).map(([team, teamTrades]) => (
              <div key={team} className="mb-4">
                <h4 className="text-lg font-medium">{team}</h4>
                <ul className="list-disc pl-5">
                  {teamTrades.map((trade, index) => (
                    <li key={index} className="text-sm">
                      {trade.type === 'buy' ? 'Bought' : 'Sold'} {trade.quantity} {trade.asset} 
                      {trade.type === 'buy' ? ' from ' : ' to '} 
                      {trade.type === 'buy' ? trade.seller : trade.buyer} for {trade.price.toFixed(2)} JC each
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
          <div>
            <h3 className="text-xl font-semibold mb-2">Events</h3>
            <ul className="list-disc pl-5">
              {events.map((event, index) => (
                <li key={index} className="mb-2">
                  <span className="font-medium">{event.name}</span>: {event.description}
                </li>
              ))}
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};

export default TradeHistoryPopup;

