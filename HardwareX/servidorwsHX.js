#!/usr/bin/env node

const fs = require('fs');
//const https = require('https');
const WebSocket = require('ws');
const ws=require('ws');
const redis=require('redis');
const client=redis.createClient({host:'raspberrypi',port:6379});
//await client.connect();

//import { WebSocketServer } from 'ws';

const wss = new ws.WebSocketServer({ port: 8087 });

(async () => {
    await client.connect();
})();

client.on('error', (err) => console.log('Redis Client Error', err));

wss.on('connection', function connection(ws) {
  ws.on('message', function incoming(message) {
  (async () => {
    var Data= await client.get('S1Plot')//Wait for data of the Remote Laboratory (RL)
    ws.send(Data);
  })();
});

  
});
