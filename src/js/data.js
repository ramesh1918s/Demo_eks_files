/**
 * data.js — Static Data: Buses, Routes, Cities
 * VayuBus Smart Bus Booking
 */

const BusData = (() => {

  const BUSES = [
    {
      id: 1,
      name: 'Shivneri Express',
      type: 'AC Sleeper · 2+1',
      dep: '06:30', arr: '11:45', dur: '5h 15m',
      price: 650,
      totalSeats: 36,
      layout: '2+1',
      decks: 2,
      tags: ['WiFi', 'AC', 'USB Charging', 'Blanket', 'Water'],
      booked: [2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35]
    },
    {
      id: 2,
      name: 'Volvo Gold Line',
      type: 'AC Semi-Sleeper · 2+2',
      dep: '09:00', arr: '15:30', dur: '6h 30m',
      price: 480,
      totalSeats: 44,
      layout: '2+2',
      decks: 1,
      tags: ['AC', 'Blanket', 'Water', 'Charging'],
      booked: [3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 36, 42]
    },
    {
      id: 3,
      name: 'Night Rider Deluxe',
      type: 'Non-AC Sleeper · 2+1',
      dep: '22:00', arr: '04:30', dur: '6h 30m',
      price: 350,
      totalSeats: 40,
      layout: '2+1',
      decks: 2,
      tags: ['Pillow', 'Blanket', 'Water'],
      booked: [1, 4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 37]
    }
  ];

  const ROUTES = {
    'Mumbai-Pune': {
      dist: '148 km', travelTime: '2h 30m',
      stops: ['Mumbai (Dadar)', 'Khopoli Toll', 'Khalapur Bypass', 'Pune (Swargate)'],
      times: ['06:30', '07:45', '08:20', '09:00']
    },
    'Mumbai-Delhi': {
      dist: '1,421 km', travelTime: '24h',
      stops: ['Mumbai (Borivali)', 'Surat', 'Vadodara', 'Jaipur', 'Delhi (Kashmere Gate)'],
      times: ['06:00', '10:30', '13:00', '21:00', '07:00']
    },
    'Bengaluru-Hyderabad': {
      dist: '575 km', travelTime: '10h',
      stops: ['Bengaluru (Majestic)', 'Kolar', 'Hindupur', 'Kurnool', 'Hyderabad (MGBS)'],
      times: ['08:00', '09:30', '11:00', '15:00', '18:30']
    },
    'Hyderabad-Chennai': {
      dist: '627 km', travelTime: '11h',
      stops: ['Hyderabad (MGBS)', 'Nalgonda', 'Ongole', 'Nellore', 'Chennai (CMBT)'],
      times: ['07:00', '09:00', '12:00', '15:00', '18:00']
    },
    'Delhi-Jaipur': {
      dist: '280 km', travelTime: '5h',
      stops: ['Delhi (Sarai Kale Khan)', 'Gurgaon Toll', 'Dharuhera', 'Jaipur (SMS)'],
      times: ['07:00', '08:00', '09:00', '12:00']
    },
    'default': {
      dist: '—', travelTime: '—',
      stops: ['Origin City', 'Midway Stop 1', 'Midway Stop 2', 'Destination City'],
      times: ['06:30', '09:00', '11:30', '14:45']
    }
  };

  const CITIES = [
    'Mumbai', 'Delhi', 'Bengaluru', 'Hyderabad', 'Chennai',
    'Pune', 'Ahmedabad', 'Kolkata', 'Jaipur'
  ];

  return { BUSES, ROUTES, CITIES };

})();
