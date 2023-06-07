// production
//insights.init('WuFrwhmdgsPVi_pq');
// dev
insights.init('nV5wDAhavc5c9DQQ');

insights.trackPages( {
  parameters: {
    locale: insights.parameters.locale(),
    screenSize: insights.parameters.screenType(),
    referrer: insights.parameters.referrer()
   }
});