'use strict';
module.exports = function makeRouter(host) {
  const router = require('express').Router();
  router.get('/status', (req, res) => res.json({ok: true, message: 'Example plugin'}));
  router.status = () => ({ok: true});
  return router;
};
